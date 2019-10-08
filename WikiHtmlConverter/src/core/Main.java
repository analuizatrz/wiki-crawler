package core;

import java.io.File;
import java.io.IOException;

import arquivo.ArquivoUtil;

public class Main {
	public static void convert(File input, File output) {
		String wikiText;
		String htmlText;
		try {
			System.out.println("Arquivo: "+input.getName());
			wikiText = ArquivoUtil.read(input);
			htmlText = new Converter().convert(wikiText);
			ArquivoUtil.write(htmlText, output, false);
		}catch (Exception e) {
			System.out.println("Erro : "+input.getName()+ " "+e.toString());
		}
	}
	public static void convert(String inputDir, String outputDir) throws IOException {
		File dir = new File(inputDir);
		File dirOutput = new File(outputDir);

		for(File arqWiki : dir.listFiles()) {
			File arqOutput = new File(dirOutput,arqWiki.getName().replaceAll("\\.txt", ".html"));
			//if(arqOutput.exists()) {
				convert(arqWiki, arqOutput);
			//}
		}
	}
	public static void main(String[] args) {
		/*
		String baseFolder = "/home/ana/Documents/tcc-collected-data/data"; 
		String inputDir = baseFolder + "/content_200701-200901-errors/data";
		String outputDir = baseFolder + "/content_200701_2009_01_html";
		*/ 
		String inputDir = "/home/ana/Downloads/input";
		String outputDir = "/home/ana/Downloads/output";

		try {
			convert(inputDir, outputDir); 
		}
		catch (Exception e) { 
			System.out.println("Erro : "+e.toString()); 
		}
	}
}
