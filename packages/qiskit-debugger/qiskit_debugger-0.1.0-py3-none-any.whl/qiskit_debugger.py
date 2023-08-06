from qiskit import Aer, execute, transpile
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

from pprint import pprint

hw_backend = None

def run_circuit(circ, simulator='qasm_simulator', use_hardware=False):
    if not use_hardware:
        backend = Aer.get_backend(simulator)
        job = execute(circ, backend, shots=1000)
        result = job.result()
    
    if use_hardware:
        hw_job1 = execute(circ, hw_backend, shots=1000)
        result = hw_job1.result()

    return result


class QCDebugger:

    def __init__(self, qc, use_hardware=False):
        """Debugger object that acts as a runner, similar to the GDB interface"""
        self.qc = qc
        self.use_hardware = use_hardware
        self.re_qc = None
        self.sub_qc = None
        self.unitary_qc = None

        self._unitary_for_next_bp = None
        self._circuit_for_next_bp = None
        self._temp_var = None
        self.counts_from_last_measurement = None
        self.remaining_breakpoints = 0
    
        if self._validate_circuit() == False:
            raise Exception("Circuit provided is cannot be used with a debugger")
            

    def _validate_circuit(self):
        """ensure there is no invalid instructions in the circuit"""
        # circuits with measurements cannot produce unitary matrix

        return True
    
    def resynthesize_circuit(self, unitary):
        """Create, transpile and ready to run"""
        nqubits = self.qc.num_qubits
        ncbits = self.qc.num_clbits
        re_qc = QuantumCircuit(nqubits, ncbits)
        re_qc.unitary(unitary, range(nqubits)) 
        re_qc = transpile(re_qc, basis_gates = ['cx', 'u3'])
        return re_qc

    def slice_circuit_beginning_to_bp(self, debug_circuit):
        if not isinstance(debug_circuit, QuantumDebugCircuit):
            raise Exception("Use QuantumDebugCircuit class to get a debuggable circuit.")
        
        bps = debug_circuit.breakpoints
        if len(bps) > 1:
            [start, end] = bps[:2]
        elif len(bps) == 1:
            end = bps[0]
        
        sliced_qc = debug_circuit.copy("subcircuit_bp_{0}_to_{1}".format(0, end))
        del sliced_qc.data[end:]
        self.unitary_qc = sliced_qc

    def slice_circuit_bp_to_bp(self, debug_circuit):
        """Call this after the slice_circuit_beginning_to_bp function"""
        if not isinstance(debug_circuit, QuantumDebugCircuit):
            raise Exception("Use QuantumDebugCircuit class to get a debuggable circuit.")
        
        bps = debug_circuit.breakpoints
        if len(bps) > 1:
            [start, end] = bps[:2]
            
        elif len(bps) == 1 and bps[0] not in [0,1]:
            start = bps[0]
            end = None
        
        sliced_qc = debug_circuit.copy("subcircuit_bp_{0}_to_{1}".format(start, end))
        if end: # when the end is the end of the circuit as well
            del sliced_qc.data[end:]
        
        del sliced_qc.data[:start]
        
        self.sub_qc = sliced_qc
        print(self.sub_qc)
        # remove the first item
        debug_circuit.breakpoints.pop(0)
        
        
    def _continue(self):
        """do a simultaneous run on simulator"""
        if len(self.qc.breakpoints) == 0:
            print("Circuit finished running.")
            return
        
        # Parallel Run 1: get unitary matrix
        self.slice_circuit_beginning_to_bp(self.qc)
        unitary_run = run_circuit(self.unitary_qc, 'unitary_simulator')
        unitary = unitary_run.get_unitary()
        
        # Parallel Run 2: get measurements
        self._temp_var = unitary # FIXME: remove this later
        self.re_qc = self.resynthesize_circuit(unitary)
        self.slice_circuit_bp_to_bp(self.qc)
  
        # FIXME: is the compose working correctly????
        self.re_qc.compose(self.sub_qc)

        # if resynthesized circuit is available, run that 
        # else run the initial circuit
        if self.re_qc:
            measure_qc = self.re_qc
        else:
            measure_qc = self.qc
        
        #print("synthesized circuit")
        #print(measure_qc)
        measure_qc.measure_all()
        probability_run_result = run_circuit(measure_qc, 'qasm_simulator', use_hardware=self.use_hardware)
        print("Probability Distribution")
        self.counts_from_last_measurement = probability_run_result.get_counts()
        print(self.counts_from_last_measurement)
        measure_qc.remove_final_measurements()
        
        self.remaining_breakpoints = len(self.qc.breakpoints)

    def c(self):
        """c(ontinue): run until the next breakpoint"""
        return self._continue()
    
    def run_all(self):
        while self.qc.breakpoints:
            print("running breakpoint")
            self.c()

class QuantumDebugCircuit(QuantumCircuit):
    def __init__(self, *args, **kwargs):
        self.breakpoints = [0,] # list of indices where the breakpoint should be at
        super(QuantumDebugCircuit, self).__init__(*args, **kwargs)
        
    def bp(self):
        if len(self.data) > 0:
            self.barrier()
            self.breakpoints.append(len(self.data) - 1)
            # add a barrier to keep a visual track
            
    
__all__ = [QCDebugger, QuantumDebugCircuit, run_circuit, hw_backend]