package main.textfiller;

import java.util.*;

public interface TextFiller {

    public int size ();
    public boolean empty ();
    public void add (String toAdd);
    public boolean contains (String query);
    public String textFill (String query);
    public List<String> getSortedList ();

}
