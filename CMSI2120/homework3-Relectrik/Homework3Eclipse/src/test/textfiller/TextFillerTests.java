package test.textfiller;

import static org.junit.Assert.*;

import org.junit.AfterClass;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestWatcher;
import org.junit.rules.Timeout;
import org.junit.runner.Description;

import main.textfiller.*;
import java.util.*;

public class TextFillerTests {
    
    // =================================================
    // Test Configuration
    // =================================================
    
    // Global timeout to prevent infinite loops from
    // crashing the test suite
    @Rule
    public Timeout globalTimeout = Timeout.seconds(2);
    
    // Used for grading, reports the total number of tests
    // passed over the total possible
    static int possible = 0, passed = 0;

    // Used as the basic empty TextFiller to test; 
    // the @Before method is run before every @Test
    TernaryTreeTextFiller tf;
    @Before
    public void init () {
        possible++;
        tf = new TernaryTreeTextFiller();
    }
    
    // Each time you pass a test, you get a point! Yay!
    // [!] Requires JUnit 4+ to run
    @Rule
    public TestWatcher watchman = new TestWatcher() {
        @Override
        protected void succeeded(Description description) {
            passed++;
        }
    };
    
    @AfterClass
    public static void gradeReport () {
        System.out.println("============================");
        System.out.println("Tests Complete");
        System.out.println(passed + " / " + possible + " passed!");
        if ((1.0 * passed / possible) >= 0.9) {
            System.out.println("[!] Nice job!"); // Automated acclaim!
        }
        System.out.println("============================");
    }
    
    
    // =================================================
    // Unit Tests
    // =================================================
    
    // Initialization Tests
    // -------------------------------------------------
    @Test
    public void testAutocompleter() {
        assertTrue(tf.empty());
    }

    // Basic Tests
    // -------------------------------------------------
    @Test
    public void testAdd_t0() {
        tf.add("is");
        tf.add("it");
        tf.add("as");
        tf.add("ass");
        tf.add("at");
        tf.add("bat");
    }
    
    @Test
    public void testSize_t0() {
        tf.add("is");
        tf.add("it");
        tf.add("as");
        assertEquals(3, tf.size());
        tf.add("as");
        assertEquals(3, tf.size());
    }

    @Test
    public void testContains_t0() {
        tf.add("is");
        tf.add("it");
        tf.add("as");
        tf.add("ass");
        tf.add("at");
        tf.add("bat");
        tf.add("bother");
        assertTrue(tf.contains("is"));
        assertTrue(tf.contains("it"));
        assertTrue(tf.contains("as"));
        assertTrue(tf.contains("ass"));
        assertTrue(tf.contains("at"));
        assertTrue(tf.contains("bat"));
        assertTrue(tf.contains("bother"));
        assertFalse(tf.contains("ii"));
        assertFalse(tf.contains("i"));
        assertFalse(tf.contains("zoo"));
    }

    @Test
    public void testTextFill_t0() {
        tf.add("is");
        tf.add("it");
        tf.add("as");
        tf.add("at");
        tf.add("item");
        tf.add("ass");
        tf.add("bat");
        tf.add("bother");
        tf.add("goat");
        tf.add("goad");
        assertEquals("is", tf.textFill("is"));
        assertEquals("it", tf.textFill("it"));
        assertEquals("item", tf.textFill("ite"));
        assertEquals("as", tf.textFill("as"));
        assertEquals("bat", tf.textFill("ba"));
        assertEquals("bother", tf.textFill("bo"));
        assertEquals(null, tf.textFill("bad"));
        assertEquals(null, tf.textFill("zoo"));
        String result = tf.textFill("go");
        assertTrue(result.equals("goat") || result.equals("goad"));
    }
    
    @Test
    public void testGetSortedList_t0() {
        tf.add("is");
        tf.add("it");
        tf.add("as");
        tf.add("itinerary");
        tf.add("ass");
        tf.add("at");
        tf.add("zoo");
        tf.add("bat");
        tf.add("bother");
        ArrayList<String> solution = new ArrayList<String>(Arrays.asList(
            "as", "ass", "at", "bat", "bother", "is", "it", "itinerary", "zoo"
        ));
        assertEquals(solution, tf.getSortedList());
    }
    
}
