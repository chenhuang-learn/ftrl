package ftrl;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

public class FTRLProximal {
	// parameters->alpha, beta, l1, l2, dimensions
	private Parameters parameters;
	// n->squared sum of past gradients
	private double[] n;
	// z->weights
	private double[] z;
	// w->lazy weights
	private Map<Integer, Double> w;

	public FTRLProximal(Parameters parameters) {
		this.parameters = parameters;
		this.n = new double[parameters.dataDimensions];
		this.z = new double[parameters.dataDimensions];
		this.w = null;
	}

	/** x->p(y=1|x; w) , get w, nothing is changed*/
	public double predict(Map<Integer, Double> x) {
		w = new HashMap<Integer, Double>();
		double decisionValue = 0.0;
		for (Entry<Integer, Double> e : x.entrySet()) {
			double sgn = sign(z[e.getKey()]);
			double weight = 0.0;
			if (sgn * z[e.getKey()] <= parameters.L1_lambda) {
				w.put(e.getKey(), weight);
			} else {
				weight = (sgn * parameters.L1_lambda - z[e.getKey()])
						/ ((parameters.beta + Math.sqrt(n[e.getKey()]))
								/ parameters.alpha + parameters.L2_lambda);
				w.put(e.getKey(), weight);
			}
			decisionValue += e.getValue() * weight;
		}
		decisionValue = Math.max(Math.min(decisionValue, 35.), -35.);
		return 1. / (1. + Math.exp(-decisionValue));
	}
	
	/** input: sample x, probability p, label y(-1(or 0) or 1) 
	 *  used: w 
	 *  update: n, z*/
	public void updateModel(Map<Integer, Double> x, double p, double y) {
		for(Entry<Integer, Double> e : x.entrySet()) {
			double grad = p * e.getValue();
			if(y == 1.0) {
				grad = (p - y) * e.getValue();
			}
			double sigma = (Math.sqrt(n[e.getKey()] + grad * grad) - 
					Math.sqrt(n[e.getKey()])) / parameters.alpha;
			z[e.getKey()] += (grad - sigma * w.get(e.getKey()));
			n[e.getKey()] += grad * grad;
		}
	}

	private double sign(double x) {
		if (x > 0) {
			return 1.0;
		} else if (x < 0) {
			return -1.0;
		} else {
			return 0.0;
		}
	}
}
