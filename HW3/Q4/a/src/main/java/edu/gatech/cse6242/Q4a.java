package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4a {

  public static class MyDegreeMapper extends Mapper<LongWritable, Text, Text, Text>{

    private final Text DID = new Text();
    private final Text PID = new Text();

    private final static Text P = new Text("pickup");
    private final static Text D = new Text("dropoff");

    public void map(final LongWritable key, final Text value, final Context context)
        throws IOException, InterruptedException {

      final String[] tokens = value.toString().split("\t");

      PID.set(tokens[0]);
      DID.set(tokens[1]);
      context.write(PID, P);
      context.write(DID, D);
    }
  }

  public static class MyDegreeReducer extends Reducer<Text, Text, Text, Text>{

    private Text key = new Text();

    public void reduce(final Text key, final Iterable<Text> values, final Context context)
        throws IOException, InterruptedException {

      int degree = 0;

      for (final Text value : values) {

        final String line = value.toString();
        final String P = "pickup";
        final String D = "dropoff";

        if (line.equals(P)) {
          degree += 1;
        } else if (line.equals(D)){
          degree -= 1;
        }
      }
      context.write(key, new Text(""+degree));
    }
  }

  public static class MySwapperMapper extends Mapper<LongWritable, Text, Text, Text>{
    // swaps the key and value s.t. the degree is now the key, and id is value 
    public void map(LongWritable key, Text value, Context context
      ) throws IOException, InterruptedException{
        //System.out.println(key.toString());
        //System.out.println(value.toString());
        String[] tokens = value.toString().split("\\s+");

        String location = tokens[0];
        String degree = tokens[1];
        //System.out.println(degree);
        //System.out.println(location);
        
        context.write(new Text(degree), new Text(location));
    }
  }

  public static class MySumReducer extends Reducer<Text, Text, IntWritable, IntWritable>{
    // sum up how many ID's have that certain degree of in/outs 
    private IntWritable intwKey = new IntWritable();
    private IntWritable intwValue = new IntWritable();

    public void reduce(Text key, Iterable<Text> values, Context context
    ) throws IOException, InterruptedException{
      int sum = 0;
      int intKey = Integer.parseInt(key.toString());

      for (Text val: values){
        sum += 1;
      }
      
      /*System.out.println("this is degrees key:");
      System.out.println(intKey);
      System.out.println("this is how many locations had it");
      System.out.println(sum);*/

      intwKey.set(intKey);
      intwValue.set(sum);
    
      context.write(intwKey, intwValue);
    }
  }

  private static final String OUTPUT_PATH = "intermediate_output";

  public static void main(final String[] args) throws Exception {
    final String gtid = "ahutter6";

    final Configuration conf = new Configuration();
    final Job job = Job.getInstance(conf, "Q4a");

    job.setJarByClass(Q4a.class);
    job.setMapperClass(MyDegreeMapper.class);
    //job.setCombinerClass(MyDegreeReducer.class);
    job.setReducerClass(MyDegreeReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(OUTPUT_PATH));

    job.waitForCompletion(true);
 
    //-- Job 2 -- // 
    final Configuration conf2 = new Configuration();
    final Job job2 = Job.getInstance(conf2, "Q4a");

    job2.setJarByClass(Q4a.class);
    job2.setMapperClass(MySwapperMapper.class);
    job2.setReducerClass(MySumReducer.class);

    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job2, new Path(OUTPUT_PATH));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));

    System.exit(job2.waitForCompletion(true) ? 0 : 1);


  }
}
