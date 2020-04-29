package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;

import java.io.IOException;
import java.text.DecimalFormat;
import java.util.StringTokenizer;

import javax.sound.sampled.FloatControl;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class Q1 {

  final String gtid = "ahutter6";

  public static class MyMapper extends Mapper<LongWritable, Text, Text, Text>{

    private Text textKey = new Text(); // New Pickup ID string
    private Text textValue = new Text();
    private final static IntWritable trip_count = new IntWritable(1); // Each PID has 1 trip in Mapper

    public void map(LongWritable key, Text value, Context context
      ) throws IOException, InterruptedException{

      String[] tokens = value.toString().split(",");
      float distance = Float.parseFloat(tokens[2]);
      float fare = Float.parseFloat(tokens[3]);

      int k = Integer.parseInt(tokens[0]);

      if (tokens.length == 4 && distance > 0 && fare > 0 && k >0){
        String data = trip_count + "," + fare;
        textKey.set(tokens[0]);
        textValue.set(data);
        context.write(textKey, textValue);
      }
    }
    }

  public static class MyReducer extends Reducer<Text, Text, Text, Text >{

    private Text finalString = new Text();

    public void reduce(Text key, Iterable<Text>values, Context context
      ) throws IOException, InterruptedException {

        int sumT = 0;
        float sumF = 0;

        DecimalFormat df = new DecimalFormat("#,###,###.00");
        for (Text value: values){
          String[] tokens = value.toString().split(",");

          int trip_count = Integer.parseInt(tokens[0]);
          float fare = Float.parseFloat(tokens[1]);
          sumT += trip_count;
          sumF += fare;
        }
        String data = sumT + "," + df.format(sumF);

        finalString.set(data);
        context.write(key, finalString);
      }
    }

  public static void main(String[] args) throws Exception {

    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");
    job.setJarByClass(Q1.class);
    job.setMapperClass(MyMapper.class);
    job.setCombinerClass(MyReducer.class);
    job.setReducerClass(MyReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
