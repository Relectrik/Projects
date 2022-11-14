package test.pathfinder.informed.trikey;

import static org.junit.Assert.*;

import org.junit.AfterClass;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestWatcher;
import org.junit.rules.Timeout;
import org.junit.runner.Description;

import java.util.*;
import main.pathfinder.informed.trikey.*;

/**
 * Unit tests for Maze Pathfinder. Tests include completeness and
 * optimality.
 */
public class PathfinderGradingTests {
    
    // =================================================
    // Test Configurations
    // =================================================
    
    public static final String SOL_ERR = "Returned solution does not solve the maze",
                               OPT_ERR = "Returned solution is suboptimal",
                               NOS_ERR = "Returned a solution where there wasn't one";
    
    // Global timeout to prevent infinite loops from
    // crashing the test suite, plus, tests to make sure
    // you're not implementing anything too computationally
    // crazy
    // [!] WARNING: Comment out these next two lines to use
    //     the debugger! Otherwise, it'll stop shortly after
    //     starting!
    @Rule
    public Timeout globalTimeout = Timeout.seconds(10);
    
    // Each time you pass a test, you get a point! Yay!
    // [!] Requires JUnit 4+ to run
    @Rule
    public TestWatcher watchman = new TestWatcher() {
        @Override
        protected void succeeded(Description description) {
            passed++;
        }
    };
    
    // Grade record-keeping
    static int possible = 0, passed = 0;
    
    // the @Before method is run before every @Test
    @Before
    public void init () {
        possible++;
    }
    
    // Used for grading, reports the total number of tests
    // passed over the total possible
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
    
    
    public static String[] createBigBoiMaze (int sizeX, int sizeY, MazeState initial, Set<MazeState> keys, Set<MazeState> mud, Set<MazeState> walls) {
        String[] result = new String[sizeY];
        int keyCount = 1;
        for (int r = 0; r < sizeY; r++) {
            String row = "";
            for (int c = 0; c < sizeX; c++) {
                MazeState current = new MazeState(c, r, null);
                if (r == 0 || r == sizeY-1 || c == 0 || c == sizeX-1 || walls.contains(current)) {
                    row += "X";
                } else if (current.equals(initial)) {
                    row += "I";
                } else if (keys.contains(current)) {
                    row += "" + keyCount++;
                } else if (mud.contains(current)) {
                    row += "M";
                } else {
                    row += ".";
                }
            }
            result[r] = row;
        }
        return result;
    }
    
    // =================================================
    // Unit Tests
    // =================================================
    
    @Test
    public void testPathfinder_t0() {
        String[] maze = {
        //   0123456
            "XXXXXXX", // 0
            "XI.1.2X", // 1
            "X.....X", // 2
            "X.X.X3X", // 3
            "XXXXXXX"  // 4
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        // result will be a 2-tuple (isSolution, cost) where
        // - isSolution = 0 if it is not, 1 if it is
        // - cost = numerical cost of proposed solution
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 6, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t1() {
        // Doesn't matter what order you collect the key pieces as long as it's
        // the optimal path between the three pieces
        String[] maze = {
        //   0123456
            "XXXXXXX", // 0
            "XI.3.2X", // 1
            "X.....X", // 2
            "X.X.X1X", // 3
            "XXXXXXX"  // 4
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 6, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t2() {
        String[] maze = {
        //   0123456
            "XXXXXXX", // 0
            "XI....X", // 1
            "X.MMM2X", // 2
            "X.X1X3X", // 3
            "XXXXXXX"  // 4
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 14, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t3() {
        String[] maze = {
        //   0123456
            "XXXXXXX", // 0
            "XI.3..X", // 1
            "XMMMM.X", // 2
            "X2X1X.X", // 3
            "XXXXXXX"  // 4
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 14, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t4() {
        String[] maze = {
        //   0123456
            "XXXXXXX", // 0
            "XI.3..X", // 1
            "X.MMM.X", // 2
            "X2X.X1X", // 3
            "XXXXXXX"  // 4
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 10, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t5() {
        String[] maze = {
        //   0123456
            "XXXXXXX", // 0
            "XI.3..X", // 1
            "X.MXM.X", // 2
            "X2X1X.X", // 3
            "XXXXXXX"  // 4
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    
    @Test
    public void testPathfinder_t6() {
        String[] maze = {
            "XXXXXXXXX",
            "XXXX.XXXX",
            "XXXX.XXXX",
            "XI...M12X",
            "XXXX.XX.X",
            "XXXX3...X",
            "XXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 11, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t7() {
        String[] maze = {
            "XXXXXXXXX",
            "XXXX1XXXX",
            "XXXX.XXXX",
            "XI.....2X",
            "XXXX.XXXX",
            "XXXX3XXXX",
            "XXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 14, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t8() {
        String[] maze = {
            "XXXXXXXXX",
            "XXX1XXXXX",
            "XXXMXXXXX",
            "XI.....2X",
            "XXXX.XXXX",
            "XXXX3XXXX",
            "XXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 18, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t9() {
        String[] maze = {
            "XXXXXXXXX",
            "XXX.1XXXX",
            "XXXMXXXXX",
            "XI.....2X",
            "XXXX.XXXX",
            "XXXX3XXXX",
            "XXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 19, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t10() {
        String[] maze = {
            "XXXXXXXXX",
            "XXX1...XX",
            "XXXMXX.XX",
            "XI...M.2X",
            "XXXX.XXXX",
            "XXXX3XXXX",
            "XXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 18, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t11() {
        String[] maze = {
            "XXXXXXXXX",
            "XXX.1XXXX",
            "XXXMXXXXX",
            "XI.....2X",
            "XXXXMXXXX",
            "XXXXM3XXX",
            "XXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]); // Test that result is a solution
        assertEquals(OPT_ERR, 26, result[1]); // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t12() {
        String[] maze = {
            "XXXXXXXXXX",
            "X...1....X",
            "XIXXXXXX2X",
            "X..M3....X",
            "XXXXXXXXXX",
            "XXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 14, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t13() {
        String[] maze = {
            "XXXXXXXXXX",
            "X...1..MMX",
            "XIXXXXXXMX",
            "X..M3.2MMX",
            "XXXXXXXXXX",
            "XXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 16, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t14() {
        String[] maze = {
            "XXXXXXXXXXX",
            "X1........X",
            "X.........X",
            "X..XMMMX..X",
            "XXXMMIMMXXX",
            "X..M2M.M.3X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 29, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t15() {
        String[] maze = {
            "XXXXXXXXXXX",
            "X1........X",
            "X...XXX...X",
            "X..XMMMX..X",
            "XXXMMIMMXXX",
            "X..M2M.M.3X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    
    @Test
    public void testPathfinder_t16() {
        String[] maze = {
            "XXXXXXXXXXX",
            "X1........X",
            "X...XXX...X",
            "X2.XMMMX.3X",
            "XXXMMIMMXXX",
            "X..M.M.M..X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    
    @Test
    public void testPathfinder_t17() {
        String[] maze = {
            "XXXXXX",
            "XI123X",
            "XXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 3, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t18() {
        String[] maze = {
            "XXXXXX",
            "X1I23X",
            "XXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 4, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t19() {
        String[] maze = {
            "XXXXXXXXXXX",
            "XMMMMMMM1MX",
            "XMMMMMMMMMX",
            "XMMMMIMMM3X",
            "XMMMMMMMMMX",
            "XMMMMMMM2MX",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 27, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t20() {
        String[] maze = {
            "XXXXXXXXXXX",
            "XMMMMMMM1MX",
            "XMMMMMMMMMX",
            "XMMMMIMMM3X",
            "XMMMMMMMMMX",
            "XMMMMMMMM2X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 24, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t21() {
        String[] maze = {
            "XXXXXXXXXXX",
            "XMMMMXMM1MX",
            "XMMMXMXMMMX",
            "XMMXMIMXM3X",
            "XMMMXMXMMMX",
            "XMMMMXMMM2X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    
    @Test
    public void testPathfinder_t22() {
        String[] maze = {
            "XXXXXXXXXXX",
            "XXXXX1MMMXX",
            "XXXXXXXXMXX",
            "XMMMM3M2M.X",
            "XMXXXXXXX.X",
            "X...I.....X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 35, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t23() {
        String[] maze = {
            "XXXXXXXXXXX",
            "XXXXX1MMMXX",
            "XXXXXXXXXXX",
            "XMXMM3M2M.X",
            "XMXXXXXXX.X",
            "X...I.....X",
            "XXXXXXXXXXX"
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    
    @Test
    public void testPathfinder_t24() {
        String[] maze = { 
            //           11111111112
            // 012345678901234567890
            "XXXXXXXXXXXXXXXXXXXXX", // 0
            "X..X....M....X..M.XIX", // 1
            "X...X..M.M..M..MM..MX", // 2
            "XMM..XMMMMM..X....X.X", // 3
            "X..M..X......X1.M...X", // 4
            "XX.......XXXXXMXXMM.X", // 5
            "X.XXX3MM...2X.X.X...X", // 6
            "X...X.MM....MXXX..XXX", // 7
            "XXM.X..MMMMMX..M..X.X", // 8
            "X.X.........X..M....X", // 9
            "XXXXXXXXXXXXXXXXXXXXX"  // 10
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 35, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t25() {
        String[] maze = { 
            //           11111111112
            // 012345678901234567890
            "XXXXXXXXXXXXXXXXXXXXX", // 0
            "X..X....M....X..M.XIX", // 1
            "X...X..M.M..M..MM..MX", // 2
            "XMM..XMMMMM..X....X.X", // 3
            "X..M..X......X..M...X", // 4
            "XX......XXXXXXMXXMM.X", // 5
            "X.XXX3MM..X2X.X.X...X", // 6
            "X...XXMMXXX.MXXX.XXXX", // 7
            "XXM.XXXXXMMMX..M..X.X", // 8
            "X.X....1....X..M....X", // 9
            "XXXXXXXXXXXXXXXXXXXXX"  // 10
        };
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    
    
    // =================================================
    // BIG Unit Tests
    // =================================================
    /*
    @Test
    public void testPathfinder_t26() {
        MazeState initial = new MazeState(1, 1, null);
        Set<MazeState> keys = new HashSet<>(
            Arrays.asList(
                new MazeState(100, 1, null),
                new MazeState(100, 100, null),
                new MazeState(1, 100, null)
            )
        );
        Set<MazeState> mud = new HashSet<>();
        Set<MazeState> walls = new HashSet<>();
        String[] maze = createBigBoiMaze(102, 102, initial, keys, mud, walls);
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 297, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t27() {
        MazeState initial = new MazeState(1, 1, null);
        Set<MazeState> keys = new HashSet<>(
            Arrays.asList(
                new MazeState(100, 1, null),
                new MazeState(100, 100, null),
                new MazeState(1, 100, null)
            )
        );
        Set<MazeState> mud = new HashSet<>(
            Arrays.asList(
                new MazeState(99, 1, null),
                new MazeState(99, 100, null),
                new MazeState(1, 99, null)
            )
        );
        Set<MazeState> walls = new HashSet<>();
        String[] maze = createBigBoiMaze(102, 102, initial, keys, mud, walls);
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 301, result[1]);  // Ensure that the solution is optimal
    }
    
    @Test
    public void testPathfinder_t28() {
        MazeState initial = new MazeState(1, 1, null);
        Set<MazeState> keys = new HashSet<>(
            Arrays.asList(
                new MazeState(100, 1, null),
                new MazeState(100, 100, null),
                new MazeState(1, 100, null)
            )
        );
        Set<MazeState> mud = new HashSet<>();
        Set<MazeState> walls = new HashSet<>(
            Arrays.asList(
                new MazeState(99, 1, null),
                new MazeState(100, 2, null)
            )
        );
        String[] maze = createBigBoiMaze(102, 102, initial, keys, mud, walls);
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        assertNull(NOS_ERR, solution); // Ensure that Pathfinder knows when there's no solution
    }
    */
    @Test
    public void testPathfinder_t29() {
        MazeState initial = new MazeState(1, 1, null);
        Set<MazeState> keys = new HashSet<>(
            Arrays.asList(
                new MazeState(500, 500, null),
                new MazeState(499, 499, null),
                new MazeState(498, 498, null)
            )
        );
        Set<MazeState> mud = new HashSet<>();
        Set<MazeState> walls = new HashSet<>();
        String[] maze = createBigBoiMaze(502, 502, initial, keys, mud, walls);
        MazeProblem prob = new MazeProblem(maze);
        List<String> solution = Pathfinder.solve(prob);
        
        int[] result = prob.testSolution(solution);
        assertEquals(SOL_ERR, 1, result[0]);  // Test that result is a solution
        assertEquals(OPT_ERR, 998, result[1]);  // Ensure that the solution is optimal
    }
    
}
