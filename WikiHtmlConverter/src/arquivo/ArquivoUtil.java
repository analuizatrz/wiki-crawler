package arquivo;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class ArquivoUtil {
	public static String read(File arquivo) throws IOException
	{
		BufferedReader in = new BufferedReader(new FileReader(arquivo));
		String str;
		StringBuilder texto = new StringBuilder();
		while ((str = in.readLine()) != null)
		{
			texto = texto.append(str + "\n");
		}
		in.close();
		
		return texto.toString();

	}
	public static void write(String text, File fileName, boolean append) throws IOException
	{
		BufferedWriter out = new BufferedWriter(new FileWriter(fileName, append),100);
		out.write(text);
		out.close();
	}
}
