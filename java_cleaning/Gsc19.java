
package gsc19;
import com.google.common.net.InternetDomainName;
import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.Reader;
import java.util.Arrays;
import java.nio.file.Files;
import java.nio.file.Paths;
import org.apache.commons.lang3.StringUtils;


/**
 *
 * @author lavanyasingh
 */
public class Gsc19 {
    
    public static String clean_url(String url) {
        if (StringUtils.isNumeric(url.replace(".", "").replace("www", "").replace(":", ""))) {return url;}
        String good_url = url.replace("/", "").replace(".static.", ".").replace("=", "").replace("|", "").replace("'", "");
        int perc = good_url.indexOf("%");
        int amp = good_url.indexOf("&");
        int index = Math.min(perc, amp) ;
        if (index == -1) { index = Math.max(perc, amp);}
        try{
            good_url = good_url.substring(0, index);}
        catch(java.lang.StringIndexOutOfBoundsException e) {}
        if (good_url.contains("wordpress") || good_url.contains("tumblr") || 
            good_url.contains("livejournal") || good_url.contains("medium")) {
            return good_url;}
        else{
            try{
                InternetDomainName owner = InternetDomainName.from(good_url).topPrivateDomain();
                good_url = owner.toString();}
            catch(java.lang.IllegalStateException | java.lang.IllegalArgumentException e ){
                if (good_url.contains(":")) {return good_url;}
                System.out.println(good_url);
                return good_url;
            }}
        return good_url ;
     }
    
    public static String [][] readIn (String path){
        try(
            Reader reader = Files.newBufferedReader(Paths.get(path));
            CSVReader csvReader = new CSVReader(reader);)
        {   String lines[][] = new String[300000][];
            String [] nextLine ;
            int i = 0;
        while ((nextLine = csvReader.readNext()) != null) {
            lines[i] = nextLine;
            i++;
        }
        return lines;
        }
        catch(Exception e){
            System.out.println(e);
        }
        return new String[300000][];
    }
    public static boolean contains(String[] items, String url){
        for (String item : items) {
            if (item == null ? url == null : item.equals(url)){
                return true;
            }
        }
        return false;
    }
    public static String[][] cleanLines(String [][] lines){
        String urls[] = new String [lines.length];
        String rows [][] = new String [lines.length][];
        int i = 0;
        int count = 0;
        while (lines[count]!= null){
            String url = clean_url(lines[count][1]);
            if (!contains(urls, url)) {
                urls[i] = url;
                i++;
                rows[i] = lines[count];
            }
            count++;
        }
        System.out.println(count);
        System.out.println(i);
        return rows;
    }
    
    public static void writeLinesOld(String [] lines) {
        try{
        CSVWriter writer = new CSVWriter(new FileWriter("test.csv"), ';');
        writer.writeNext(lines);
        writer.close();}
        catch(Exception e) {}
    }
    public static String makeRow(String [] line) {
        String row = "" ;
        int i = 0;
        while (i < line.length && line[i] != null) {
            row += line[i] + ",";
            i ++;
        }
        return row;
    }
    
    public static void writeLines(String [][] lines) {
       int i = 0;
       try{
        CSVWriter writer = new CSVWriter(new FileWriter("all_raw_cleaned2.csv"), ',');
        for (String[] line : lines) {
           if (line == null && i > 0) {
               System.out.print("phooey");      
               System.out.println(i);
               break;}
           writer.writeNext(line);
           i++;
       }
        writer.close();}
        catch(Exception e) {}
    }
    
    
    public static void main(String[] args) {
       String [][] s = cleanLines(readIn("all_raw_cleaned.csv"));
       writeLines(s);
        /*try{
        CSVWriter writer = new CSVWriter(new FileWriter("test.csv"), ',');
        String test [] = {"hello", "hi", "1, 2, 3"};
        writer.writeNext( test);
        writer.close();}
        catch(Exception e) {}*/
    }
    
    
}
