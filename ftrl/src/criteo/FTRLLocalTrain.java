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

public class FTRLLocalTrain {
	private FTRLProximal learner;
	private LogLossEvalutor evalutor;
	private int printInterval;
	
	public FTRLLocalTrain(FTRLProximal learner, LogLossEvalutor evalutor, int interval) {
		this.learner = learner;
		this.evalutor = evalutor;
		this.printInterval = interval;
	}
	
	public void train(String trainFile) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(new File(trainFile)), "UTF-8"));
		String line = null;
		int trainedNum = 0;
		double totalLoss = 0.0;
		long startTime = System.currentTimeMillis();
		while((line = br.readLine()) != null) {
			String[] fields = line.split(" ");
			
			double y = (Integer.parseInt(fields[0]) == 1) ? 1. : -1.;
			Map<Integer, Double> x = new HashMap<Integer, Double>();
			x.put(0, 1.);
			for(int i=1; i<fields.length; i++) {
				x.put(Integer.parseInt(fields[i]), 1.);
			}
			
			double p = learner.predict(x);
			learner.updateModel(x, p, y);
			
			double loss = LogLossEvalutor.calLogLoss(p, y);
			evalutor.addLogLoss(loss);
			totalLoss += loss;
			
			trainedNum += 1;
			if(trainedNum % printInterval == 0) {
				long currentTime = System.currentTimeMillis();
				double minutes = (double)(currentTime - startTime) / 60000;
				System.out.printf("%.3f, %.5f\n", minutes, evalutor.getAverageLogLoss());
			}
		}
		System.out.printf("global average loss: %.5f\n", totalLoss/trainedNum);
		br.close();
	}
	
	public static void main(String[] args) throws IOException {
		// need trainFile, L1, L2, alpha, dataMaxIndex
		if(args.length != 5) {
			System.out.println("java -jar ftrl_train.jar trainFile L1 L2 alpha dataMaxIndex\n"
					+ "for example:\n"
					+ "java -jar ftrl_train.jar train 1.0 1.0 0.1 1e6");
		}
		String trainFile = args[0];
		double L1 = Double.parseDouble(args[1]);
		double L2 = Double.parseDouble(args[2]);
		double alpha = Double.parseDouble(args[3]);
		int dataDimensions = Integer.parseInt(args[4]) + 1;
		double beta = 1.0;
		int testDataSize = 250000;
		int interval = 50000;
		Parameters paras = new Parameters(alpha, beta, L1, L2, dataDimensions);
		FTRLProximal learner = new FTRLProximal(paras);
		LogLossEvalutor evalutor = new LogLossEvalutor(testDataSize);
		FTRLLocalTrain trainer = new FTRLLocalTrain(learner, evalutor, interval);
		trainer.train(trainFile);
	}
	
}
