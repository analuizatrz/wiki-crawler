package core;

import py4j.GatewayServer;

public class EntryPoint {

	EntryPoint(){
		converter = new Converter();	
	}

	private Converter converter;
	
	public Converter getConverter() {
        return converter;
    }
	public static void main(String[] args) {
		System.out.println("oi");
	    GatewayServer gatewayServer = new GatewayServer(new EntryPoint());
	    gatewayServer.start();
	    System.out.println("Gateway Server Started : WikiHtmlConverter");		

	}
}
