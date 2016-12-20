import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

/*
 * Mumbling Martians - CS170 programming project
 * Due 10/10
 * 
 * @Yicheng Chen
 * @26943685
 */

public class Hw5 {

    /**
     * @param dictionary  maps Martian words to English words
     */

    public HashMap<String, String> dict;

    public Hw5(HashMap<String, String> dictionary) {
        dict = dictionary;
    }

    /**
     * Find a valid translation of s, breaking ties by shortest earliest word
     * 
     * @param s  the query (Martian) string to translate
     * @return   the translated (English) string
     */
    public String translate(String s) {
        int size = s.length();
        if (size == 0) {
            return null;
        }
        // initialize arrays
        boolean[] b = new boolean[size+1];
        int[] pos = new int[size+1];
        Arrays.fill(b, false);
        Arrays.fill(pos, -1);

        b[size] = true;

        for (int i = size - 1; i >= 0; i--) {
            if (isWord(s, i, size)) {
                b[i] = true;
                pos[i] = size;
            }
            for (int j = i + 1; j <= size; j++) {
                if (isWord(s, i, j) && b[j]) {
                    b[i] = true;
                    pos[i] = j;
                    break;
                }
            }
        }

        String result = "";
        if (b[0]) {
            int start = 0;
            while (start < size) {
                String sub = s.substring(start, pos[start]);
                result += dict.get(sub) + " ";
                start = pos[start];
            }
            result = result.substring(0, result.length() - 1);
        }
        return result;
    }
    
    /**
     * Compute the number of possible translations of s
     * 
     * @param s  the query (Martian) string
     * @return   the number of possible translations
     */
    public int numInterpretations(String s) {
        int size = s.length();
        int[] ways = new int[size+1];
        for (int i = 1; i <= size; i++) {
            for (int j = 1; j < i; j++) {
                if (isWord(s, j, i))
                ways[i] += ways[j];
            }
            if (isWord(s, 0, i)) {
                ways[i] += 1;
            }
        }
        return ways[size];
    }

    private boolean isWord(String s, int first, int last) {
        String sub = s.substring(first, last);
        return dict.containsKey(sub);
    }

    /**
     * Handles IO, you shouldn't need to touch this. 
     */
    public static void main(String[] args) {
        if (args.length != 3) {
            System.err.println("Usage: java Hw5 INPUT_FILE OUTPUT_TRANSLATE_FILE"
                    + "OUTPUT_NUM_INTERPRETATIONS_FILE");
            return;
        }
        String inputFilename = args[0];
        String translationFilename = args[1];
        String interpretationsFilename = args[2];
        File inputFile = new File(inputFilename);
        Scanner in;
        try {
            in = new Scanner(inputFile);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }
        int m = in.nextInt();
        HashMap<String, String> dictionary = new HashMap<>();
        List<String> queries = new ArrayList<>();
        for (int i = 0; i < m; i++) {
            String martianWord = in.next();
            String englishWord = in.next();
            dictionary.put(martianWord, englishWord);
        }
        while (in.hasNext()) {
            queries.add(in.next());
        }
        in.close();
        Hw5 solver = new Hw5(dictionary);
        FileWriter translationsOut;
        try {
            translationsOut = new FileWriter(translationFilename);
            FileWriter interpretationsOut = new FileWriter(interpretationsFilename);
            for (String query : queries) {
                translationsOut.write(solver.translate(query) + "\n");
                interpretationsOut.write(solver.numInterpretations(query) + "\n");
            }
            translationsOut.close();
            interpretationsOut.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
