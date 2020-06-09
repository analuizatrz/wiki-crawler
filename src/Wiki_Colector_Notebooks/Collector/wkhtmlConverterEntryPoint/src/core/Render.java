package core;

import info.bliki.wiki.model.WikiModel;

public class Render {
	private static WikiModel wikiModel = new WikiModel("http://en.wikipedia.org/wiki/${image}", "/wiki/${title}");
		
		public static String wikiToHtml(String text)
		{
			return wikiModel.render(text);
		}

}