package criteo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

import ftrl.FTRLProximal;
import ftrl.LogLossEvalutor;
import ftrl.Parameters;

public class FTRLBatchTrain {
	private FTRLProximal learner;
	
	public FTRLBatchTrain(FTRLProximal learner) {
		this.learner = learner;
	}
	
	public double process(String fileName, boolean update) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(
				new FileInputStream(new File(fileName)), "UTF-8"));
		String line = null;
		double total_loss = 0.;
		int num_samples = 0;
		while((line=br.readLine()) != null) {
			String[] fields = line.split(" ");
			
			double y = (Integer.parseInt(fields[0]) > 0) ? 1. : -1.;
			Map<Integer, Double> x = new HashMap<Integer, Double>();
			for(int i=1; i<fields.length; i++) {
				x.put(Integer.parseInt(fields[i]), 1.);
			}
			
			double p = learner.predict(x);
			if(update) {
				learner.updateModel(x, p, y);
			}
			
			
			total_loss += LogLossEvalutor.calLogLoss(p, y);
			num_samples += 1;
		}
		br.close();
		return total_loss/num_samples;
	}
	
	public void train(String trainFile, String validationFile, int iter) throws IOException {
		long startTime = System.currentTimeMillis();
		for(int it=0; it<iter; it++) {
			double tr_loss = process(trainFile, true);
			double va_loss = process(validationFile, false);
			long currentTime = System.currentTimeMillis();
			double minutes = (double)(currentTime-startTime)/60000;
			System.out.printf("iter: %2d, used_time: %.3f, tr_loss: %.5f, va_loss: %.5f\n",
					it, minutes, tr_loss, va_loss);
		}
	}
	
	public static void main(String[] args) throws IOException {
		if(args.length != 6) {
			System.out.println("java -jar ftrl_batch_train.jar trainFile validationFile L1 L2 alpha dataMaxIndex\n"
					+ "for example:\n"
					+ "java -jar ftrl_batch_train.jar tr te 1.0 1.0 0.1 1e6");
		}
		String trainFile = args[0];
		String testFile = args[1];
		double L1 = Double.parseDouble(args[2]);
		double L2 = Double.parseDouble(args[3]);
		double alpha = Double.parseDouble(args[4]);
		int dataDimensions = Integer.parseInt(args[5]) + 1;
		double beta = 1.0;
		Parameters param = new Parameters(alpha, beta, L1, L2, dataDimensions);
		FTRLProximal learner = new FTRLProximal(param);
		FTRLBatchTrain trainer = new FTRLBatchTrain(learner);
		trainer.train(trainFile, testFile, 10);
	}
}
