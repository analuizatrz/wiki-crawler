package core;

import wikiutil.WikiUtil;

public class Converter {
	public String convert(String wikiText) {
		String htmlText = WikiUtil.wikiToHtml(wikiText);
		
		htmlText = htmlText.replaceAll("<h2>", "<h1>");
		htmlText = htmlText.replaceAll("</h2>", "</h1>");
		
		htmlText = htmlText.replaceAll("<h3>", "<h2>");
		htmlText = htmlText.replaceAll("</h3>", "</h2>");
		
		return htmlText;
	}
}
