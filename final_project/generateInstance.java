import java.io.*;
import java.util.Random;

/* 
This java class generates the Horsing Around instance with given number n of vertices and 
the probability p that edge between each vertex exists. 

Usage: java generateInstance 100 0.4 cyc1
						   n   p   output_filename_base

Written by Yicheng Chen
11/19/2016

*/

public class generateInstance {

	public static void main(String[] args) {
		// default setting
		int n = 100;
        double p = 0.6;
        String fname = "cyc1.in";
        // read input setting
		if (args.length == 3) {
        	n = Integer.parseInt(args[0]);
        	p = Double.parseDouble(args[1]);
        	fname = args[2] + ".in";
        }

        System.out.println("Generating problem with " + n + " nodes");
        System.out.println("P = " + p);
        System.out.println("Output filename: " + fname);

        Random vertexGenerator = new Random();
        Random edgeGenerator = new Random();
        double edge;
        int vertex;

        try{
		    PrintWriter writer = new PrintWriter(fname);
		    
		    writer.println(n);

		    for (int i = 0; i < n; i++) {
		    	for (int j = 0; j < i; j++) {
		    		edge = edgeGenerator.nextDouble();
		    		if (edge <= p) {
		    			writer.print("1 ");
		    		} else {
		    			writer.print("0 ");
		    		}
		    	}
		    	vertex = vertexGenerator.nextInt(99)+1;
		    	writer.print(vertex + " ");
		    	for (int j = i+1; j < n; j++) {
		    		edge = edgeGenerator.nextDouble();
		    		if (edge <= p) {
		    			writer.print("1 ");
		    		} else {
		    			writer.print("0 ");
		    		}
		    	}
		    	writer.println();
		    }

		    writer.close();
		} catch (Exception e) {
		   	System.out.println("File write error occurred.");
		}

	}

}