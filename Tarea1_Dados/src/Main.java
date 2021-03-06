import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartFrame;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.statistics.HistogramDataset;

public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		int[] numeroLanzamientos = {10, 100, 1000, 10000, 100000, 1000000};
		
		for (int lanzamiento: numeroLanzamientos) {
			HistogramDataset histograma = new HistogramDataset();
			double[] resultados = new double[lanzamiento];
			
			for (int i = 0; i < lanzamiento; i++) {
				resultados[i] = lanzarDados();
			}
			histograma.addSeries("Lanzamiento dados", resultados, 11);
			
			JFreeChart c = ChartFactory.createHistogram(
	                lanzamiento + " lanzamientos",
	                "Sumatoria dados",
	                "Repeticiones",
	                histograma,
	                PlotOrientation.VERTICAL, true, true, false);

	        ChartFrame f = new ChartFrame("TAREA 1 - DADOS", c);
	        f.pack();
	        f.setVisible(true);
			
		}

	}
	
	static int lanzarDados() {
		return ((int) (Math.random() * 6) + 1) + ((int) (Math.random() * 6) + 1);
	}

}
