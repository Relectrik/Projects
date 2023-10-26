package main.csp;

import java.time.LocalDate;
import java.util.*;

/**
 * CSP: Calendar Satisfaction Problem Solver
 * Provides a solution for scheduling some n meetings in a given
 * period of time and according to some unary and binary constraints
 * on the dates of each meeting.
 */
public class CSPSolver {

    // Backtracking CSP Solver
    // --------------------------------------------------------------------------------------------------------------
    
    /**
     * Public interface for the CSP solver in which the number of meetings,
     * range of allowable dates for each meeting, and constraints on meeting
     * times are specified.
     * @param nMeetings The number of meetings that must be scheduled, indexed from 0 to n-1
     * @param rangeStart The start date (inclusive) of the domains of each of the n meeting-variables
     * @param rangeEnd The end date (inclusive) of the domains of each of the n meeting-variables
     * @param constraints Date constraints on the meeting times (unary and binary for this assignment)
     * @return A list of dates that satisfies each of the constraints for each of the n meetings,
     *         indexed by the variable they satisfy, or null if no solution exists.
     */
    public static List<LocalDate> solve (int nMeetings, LocalDate rangeStart, LocalDate rangeEnd, Set<DateConstraint> constraints) {
    	List<MeetingDomain> indexDomain = createMeetingDomainList(nMeetings, rangeStart, rangeEnd);
    	nodeConsistency(indexDomain, constraints);
    	arcConsistency(indexDomain, constraints);
    	return solveRecursively(nMeetings, constraints, new ArrayList<LocalDate>(nMeetings), indexDomain);
    }
    
	/**
	 * Recursive solver passed in from solve method to give a list of dates that satisfies constraints 
	 * for each of the n meetings.
	 * @param nMeetings The number of meetings that must be scheduled, indexed from 0 to n-1
	 * @param constraints Date constraints on the meeting times
	 * @param assignments Empty list with size of n, that will be filled recursively
	 * @param individualDomains List of MeetingDomains
	 * @return
	 */
    private static List<LocalDate> solveRecursively (int nMeetings, Set<DateConstraint> constraints, List<LocalDate> assignments, List<MeetingDomain> individualDomains) {
    	if (assignments.size() == nMeetings) {
    	    return assignments;
    	}
    	for (MeetingDomain domain : individualDomains) {
			for (LocalDate date : domain.domainValues) {
				if (isConsistent(date, constraints, assignments)) {
					assignments.add(date);
					List<LocalDate> results = solveRecursively(nMeetings, constraints, assignments, individualDomains);
					if (results != null) {
						return results;
					}
					assignments.remove(assignments.size()-1);
				}
			}
    	}
    	return null;
    	}
    
	/**
	 * Function to check if given date is consistent with the current assignments.
	 * @param date Date to check consistency for.
	 * @param constraints Set of constraints to satisfy.
	 * @param assignments Current date assignments.
	 * @return Returns true if this date is consistent with the assignments, false otherwise.
	 */
    private static boolean isConsistent(LocalDate date, Set<DateConstraint> constraints, List<LocalDate> assignments) { 
    	assignments.add(date);
    	for (DateConstraint constraint : constraints) {
    	    if (constraint.arity() == 1) {
    		UnaryDateConstraint unaryConstraint = (UnaryDateConstraint) constraint;
    		try {
    		    assignments.get(unaryConstraint.L_VAL);
    		} 
    		catch (IndexOutOfBoundsException e) {
    		    continue;
    		}
    		if (constraint.isSatisfiedBy(assignments.get(unaryConstraint.L_VAL), unaryConstraint.R_VAL)) {
    		    continue;
    		}
    		else {
    		    assignments.remove(assignments.size()-1);
    		    return false;
	        }
    	    }
    	    else {
				BinaryDateConstraint binaryConstraint = (BinaryDateConstraint) constraint;
				try {
					assignments.get(binaryConstraint.L_VAL);
					assignments.get(binaryConstraint.R_VAL);
				}
				catch (IndexOutOfBoundsException e){
					continue;
				}
				if (constraint.isSatisfiedBy(assignments.get(binaryConstraint.L_VAL), assignments.get(binaryConstraint.R_VAL))) {
					continue;
				}
				else {
					assignments.remove(assignments.size()-1);
					return false;
				}
    	    }
        }
    	assignments.remove(assignments.size()-1);
    	return true;
    }

	/**
	 * Creates an ArrayList of MeetingDomains from given range and number of meetings
	 * 
	 * @param nMeetings Number of meetings to add to list
	 * @param rangeStart Start of range
	 * @param rangeEnd End of range
	 * @return Returns the ArrayList of MeetingDomains
	 */
    private static List<MeetingDomain> createMeetingDomainList(int nMeetings, LocalDate rangeStart, LocalDate rangeEnd) {
    	List<MeetingDomain> meetingDomainsList = new ArrayList<>();
    	for (int i = 0; i < nMeetings; i++) {
    	    meetingDomainsList.add(new MeetingDomain(rangeStart, rangeEnd));
    	}
    	return meetingDomainsList;
    }
     
    // Filtering Operations
    // --------------------------------------------------------------------------------------------------------------
    
    /**
     * Enforces node consistency for all variables' domains given in varDomains based on
     * the given constraints. Meetings' domains correspond to their index in the varDomains List.
     * @param varDomains List of MeetingDomains in which index i corresponds to D_i
     * @param constraints Set of DateConstraints specifying how the domains should be constrained.
     * [!] Note, these may be either unary or binary constraints, but this method should only process
     *     the *unary* constraints! 
     */
    public static void nodeConsistency (List<MeetingDomain> varDomains, Set<DateConstraint> constraints) {
    	for (DateConstraint constraint : constraints) {
    	    if (constraint.arity() == 1) {
				UnaryDateConstraint unaryConstraint = (UnaryDateConstraint) constraint;
				MeetingDomain indexDomain = varDomains.get(unaryConstraint.L_VAL);
				MeetingDomain indexDomainCopy = new MeetingDomain(varDomains.get(unaryConstraint.L_VAL));
				for (LocalDate date : indexDomainCopy.domainValues) {
					if (!unaryConstraint.isSatisfiedBy(date, unaryConstraint.R_VAL)) {
						indexDomain.domainValues.remove(date);
					}
				}
    	    }
        }
    }
    
    /**
     * Enforces arc consistency for all variables' domains given in varDomains based on
     * the given constraints. Meetings' domains correspond to their index in the varDomains List.
     * @param varDomains List of MeetingDomains in which index i corresponds to D_i
     * @param constraints Set of DateConstraints specifying how the domains should be constrained.
     * [!] Note, these may be either unary or binary constraints, but this method should only process
     *     the *binary* constraints using the AC-3 algorithm! 
     */
    public static void arcConsistency (List<MeetingDomain> varDomains, Set<DateConstraint> constraints) {
    	Set<Arc> arcQueue = new HashSet<>();
    	for (DateConstraint constraint : constraints) {
    	    if (constraint.arity() == 2) {
    			BinaryDateConstraint binaryConstraint = (BinaryDateConstraint) constraint;
    			arcQueue.add(new Arc(binaryConstraint.L_VAL, binaryConstraint.R_VAL, constraint));
    			arcQueue.add(new Arc(binaryConstraint.R_VAL, binaryConstraint.L_VAL, (DateConstraint) binaryConstraint.getReverse()));    		
    	    }
    	}
    	emptyArcQueue(arcQueue, varDomains, constraints);
    }
    /**
	 * Removes any inconsistent arcs in the queue
	 * @param arcQueue Given populated ArcQueue
	 * @param varDomains List of MeetingDomains in which index i corresponds to D_i
	 * @param constraints Set of DateConstraints specifying how the domains should be constrained.
	 */
    private static void emptyArcQueue(Set<Arc> arcQueue, List<MeetingDomain> varDomains, Set<DateConstraint> constraints) {
    	while (!arcQueue.isEmpty()) {
    	    Arc polledArc = arcQueue.iterator().next();
    	    arcQueue.remove(polledArc);
    	    if (removeInconsistent(polledArc, varDomains)) {
				for (DateConstraint constraint : constraints) {
	       	    	if (constraint.arity() == 2) {
		        		BinaryDateConstraint binaryConstraint = (BinaryDateConstraint) constraint;
		        		if (binaryConstraint.L_VAL == polledArc.TAIL) {
		       	    		arcQueue.add(new Arc(binaryConstraint.R_VAL, binaryConstraint.L_VAL, (DateConstraint) binaryConstraint.getReverse()));
						}
						if (binaryConstraint.R_VAL == polledArc.TAIL) {
		            		arcQueue.add(new Arc(binaryConstraint.L_VAL, binaryConstraint.R_VAL, constraint));
						}
	 	    		}
				}
    	    }
    	}
    }
    
	/**
	 * Checks if the arc is inconsistent
	 * @param arc The given arc
	 * @param varDomains List of MeetingDomains in which index i corresponds to D_i
	 * @return Returns true if inconsistent, otherwise false
	 */
    private static boolean removeInconsistent (Arc arc, List<MeetingDomain> varDomains) {
    	boolean removed = false;
    	int count = 0;
    	MeetingDomain tailDomainCopy = new MeetingDomain(varDomains.get(arc.TAIL));
    	MeetingDomain tailDomain = varDomains.get(arc.TAIL);
	    for (LocalDate tailDate : tailDomainCopy.domainValues) {
			for (LocalDate headDate : varDomains.get(arc.HEAD).domainValues) {
				if (!arc.CONSTRAINT.isSatisfiedBy(tailDate, headDate)) {
			    count++;
				}
			}
			if (count == varDomains.get(arc.HEAD).domainValues.size()) {
		    	tailDomain.domainValues.remove(tailDate);
		    	removed = true;
			}
		count = 0;
	    }
	return removed;
    }
    
    /**
     * Private helper class organizing Arcs as defined by the AC-3 algorithm, useful for implementing the
     * arcConsistency method.
     * [!] You may modify this class however you'd like, its basis is just a suggestion that will indeed work.
     */
    private static class Arc {
        
        public final DateConstraint CONSTRAINT;
        public final int TAIL, HEAD;
        
        /**
         * Constructs a new Arc (tail -> head) where head and tail are the meeting indexes
         * corresponding with Meeting variables and their associated domains.
         * @param tail Meeting index of the tail
         * @param head Meeting index of the head
         * @param c Constraint represented by this Arc.
         * [!] WARNING: A DateConstraint's isSatisfiedBy method is parameterized as:
         * isSatisfiedBy (LocalDate leftDate, LocalDate rightDate), meaning L_VAL for the first
         * parameter and R_VAL for the second. Be careful with this when creating Arcs that reverse
         * direction. You may find the BinaryDateConstraint's getReverse method useful here.
         */
        public Arc (int tail, int head, DateConstraint c) {
            this.TAIL = tail;
            this.HEAD = head;
            this.CONSTRAINT = c;
        }
        
        @Override
        public boolean equals (Object other) {
            if (this == other) { return true; }
            if (this.getClass() != other.getClass()) { return false; }
            Arc otherArc = (Arc) other;
            return this.TAIL == otherArc.TAIL && this.HEAD == otherArc.HEAD && this.CONSTRAINT.equals(otherArc.CONSTRAINT);
        }
        
        @Override
        public int hashCode () {
            return Objects.hash(this.TAIL, this.HEAD, this.CONSTRAINT);
        }
        
        @Override
        public String toString () {
            return "(" + this.TAIL + " -> " + this.HEAD + ")";
        }
        
    }
    
}
