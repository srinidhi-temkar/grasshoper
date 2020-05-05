import java.io.IOException;
import java.io.*;
import java.util.*;
import java.lang.*;

import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.*;


public class GreenPartCount {
	public static class GreenPartMapper
        	extends Mapper<LongWritable,Text,Text,IntWritable>{
        	
        	private final static IntWritable one = new IntWritable(1);

    	
    		public void map(LongWritable key, Text value, Context context
                    ) throws IOException, InterruptedException {
        		String line = value.toString();
			String[] arrOfString = line.split(",");
			
        	float percentage = Float.parseFloat(arrOfString[0].trim());
			String ward = arrOfString[1];
				

    		if (percentage <= 25.0f) {
 			context.write(new Text("0-25%"),one);
 			}
 			else if((percentage > 25.0f) && (percentage <= 33.0f))
 				context.write(new Text("25-33%"),one);
 			else if((percentage > 33.0f) && (percentage <= 50.0f))
 				context.write(new Text("33-50%"),one);
 			else if((percentage > 50.0f) && (percentage <= 75.0f))
 				context.write(new Text("50-75%"),one);
 			else
 				context.write(new Text("75-100%"),one);
    		}
	}
	
	public static class GreenPartReducer
        		extends Reducer<Text,IntWritable ,Text,IntWritable>{
        	 private IntWritable result = new IntWritable();
    		
    		public void reduce(  Text key,Iterable<IntWritable> value, Context context
                       ) throws IOException, InterruptedException {
                     
                  int sum = 0;
				  for (IntWritable val : value) {
					sum += val.get();
				  }
				  result.set(sum);
     			 context.write(key, result);
				
			
		}
	}

	public static void main(String[]args) throws Exception {
		Configuration conf = new Configuration();
		conf.addResource(new Path("/Input/"));
		Job job = Job.getInstance(conf, "greenpartcount");
		job.setJarByClass(GreenPartCount.class);
		job.setMapperClass(GreenPartMapper.class);
		job.setCombinerClass(GreenPartReducer.class);
		job.setReducerClass(GreenPartReducer.class);
		 job.setMapOutputKeyClass(Text.class);
		 job.setMapOutputValueClass(IntWritable.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
