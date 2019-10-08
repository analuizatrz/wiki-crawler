package core;

import py4j.GatewayServer;

public class EntryPoint {
	public static void main(String[] args) {
	    GatewayServer gatewayServer = new GatewayServer(new EntryPoint());
	    gatewayServer.start();
	    System.out.println("Gateway Server Started : WikiHtmlConverter");		
	}
	EntryPoint(){
		converter = new Converter();	
	}

	private Converter converter;
	
	public Converter getConverter() {
        return converter;
    }

}

