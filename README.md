<h1 style="text-align: center;">Visualizing Provenance to Support Exploratory Trade-off Analysis</h1>
<h4><code>Trade-off Analysis</code></h4>
<p><strong style="color: #000;"></strong></p>

<p> 
  <em> Note: We have provided the python code (DataVis.py) and an example dataset (ExampleInput.xml) above. If you want to run the project  on your machine you just need to install <a href="https://dash.plot.ly/installation">Dash</a> then execute the code as you would any python code (see demo video). </em>
</p>

<hr>

<p>
  <strong style="color: #000;">Goal: </strong>This project aims to create a visualization for domain experts wanting to understand their own analysis or exploration processes (reflection). In other words we are trying to highlight patterns in their explorations.
</p>

<hr>

<p>
  <strong style="color: #000;">The Dataset: </strong> Automatically generated log files of user interactions with a visualization tool (124k lines of xml, 17 fields). The data was collected during four interactive exploration sessions of agronomy models with domain experts. The experts wanted to analyse various trade-off scenarios. 
</p>

<hr>

<p>
  <strong style="color: #000;">Our visualisation choice</strong>: A parallel axis graph that shows the patterns in the actions and dimensions with the ability to filter the data and explore different lengths of patterns.
</p>

![ImageEx](/ScreenExample3.PNG?raw=true "Optional Title")

<p>The darker a stripe is, the higher its count is. the count represents the number of times a pattern has been seen in the data. the parallel axis contain the actions that constitute the paterns</p>


<p><strong style="color: #000;">Interaction &amp; Filters:<br /></strong></p>
<ul>
<li>The ability to load any Xml log file.</li>
<li>The ability to generate a graph for actions or dimensions.</li>
<li>The patterns are highlighted on mouse hover and their counts are displayed</li>
<li>The ability to choose the length of the patterns to display (2-10) .</li>
<li>Min/max filters for the pattern counts.</li>
<li>Inclusion/Exclusion filters for the actions (not yet implemented for dimensions).</li>
<li>"No loop" filter to remove the instances where an action loops over itself.</li>
</ul>
<p><strong style="color: #000;">Video Demo (Previous version|before reviews):</strong>&nbsp;<br /><a href="https://www.youtube.com/watch?v=p8_xa7Fg_ww&amp;feature=youtu.be">https://www.youtube.com/watch?v=p8_xa7Fg_ww&amp;feature=youtu.be</a></p>
<p></p>

# How to run:

## Dependecies:

### Python 3.7:
The code for this project was made using python 3.7

### Dash 1.8.0:
[install Dash](https://dash.plot.ly/installation)

### Plotly 4.5.2:
Plotly should be installed automatically once you install Dash but if for some reason you do not have it even after installing Dash here is the [Link to install Plotly](https://plot.ly/python/getting-started/) 

### Pandas 0.24.2
[install Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

## Running:
-Download DataVis.py and ExampleInput.xml.  
-Run DataVis.py with the command ` python DataVis.py`  
-The program will launch a local server and give you the address it is running at    
-Copy the address in your browser of choice  
-Done! you can upload ExampleInput.xml with the file chooser and interact with the visualisation.  
     
     
      
    
    
 
