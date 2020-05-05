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
        	extends Mapper<LongWritable,Text, FloatWritable, Text>{

    		//@Override
    		public void map(LongWritable key, Text value, Context context
                    ) throws IOException, InterruptedException {
        		String line = value.toString();
			String[] arrOfString = line.split(",");
			
        		float percentage = Float.parseFloat(arrOfString[0].trim());
			String ward = arrOfString[1];
				

    			if (percentage > 33.0f) {
 			context.write(new FloatWritable(percentage), new Text(ward));
			
        		}
    		}
	}
	
	public static class MaxTemperatureReducer
        		extends Reducer<FloatWritable, Text, Text, FloatWritable>{
    		//@Override
    		public void reduce(FloatWritable value, Text key,  Context context
                       ) throws IOException, InterruptedException {
				context.write(key,value);
			
		}
	}

	public static void main(String[]args) throws Exception {
		Configuration conf = new Configuration();
		conf.addResource(new Path("/Input/"));
		Job job = Job.getInstance(conf, "greenpartcount");
		job.setJarByClass(GreenPartCount.class);
		job.setMapperClass(GreenPartMapper.class);
		job.setCombinerClass(MaxTemperatureReducer.class);
		job.setReducerClass(MaxTemperatureReducer.class);
		job.setNumReduceTasks(0);
		job.setMapOutputKeyClass(FloatWritable.class);
		job.setMapOutputValueClass(Text.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FloatWritable.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
