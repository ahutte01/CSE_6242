package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

import java.text.DecimalFormat; // I added this piece

public class Q4b {

  public static class MyPassengerMapper extends Mapper<LongWritable, Text, Text, Text>{
  
  private final Text passcount = new Text();
  private final Text fare = new Text();

  public void map(final LongWritable key, final Text value, final Context context)
    throws IOException, InterruptedException {

      final String[] tokens = value.toString().split("\t");

      passcount.set(tokens[2]);
      fare.set(tokens[3]);

      context.write(passcount, fare);
    }
  }

  public static class MyFareReducer extends Reducer<Text, Text, IntWritable, Text>{

    private final IntWritable passcount = new IntWritable();
    private final Text avgfare = new Text();

    public void reduce(Text key,  Iterable<Text> values, final Context context)
      throws IOException, InterruptedException{

        int count = 0;
        double sum = 0;

        DecimalFormat df = new DecimalFormat("0.00");
        for (final Text value: values){
          count += 1;
          sum += Double.parseDouble(value.toString());
        }

        double avg = (sum / count);
        String stravg = df.format(avg);
        
        int intkey = Integer.parseInt(key.toString());

        passcount.set(intkey);
        avgfare.set(stravg);

        context.write(passcount, avgfare);
      }
  }

  public static void main(String[] args) throws Exception {

    final String gtid = "ahutter6";

    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4b");

    job.setJarByClass(Q4b.class);
    job.setMapperClass(MyPassengerMapper.class);
    job.setReducerClass(MyFareReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
