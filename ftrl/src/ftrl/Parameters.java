package ftrl;

public class Parameters {
	public double alpha;
	public double beta;
	public double L1_lambda;
	public double L2_lambda;
	public int dataDimensions;
	
	public Parameters(double alpha, double beta, 
			double L1, double L2, int dataDimensions) {
		this.alpha = alpha;
		this.beta = beta;
		this.L1_lambda = L1;
		this.L2_lambda = L2;
		this.dataDimensions = dataDimensions;
	}
}
