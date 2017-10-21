<h1>sppIDer</h1>

<p>A tool to identify species and inter-species hybrids and chromosome copy number variants from short-read data.</p>

<p>This tool is still a draft version therefore there are many known issues with accessing and running sppIDer I am actively working to inprove.</p>

<p>sppIDer.py is the main wrapper that calls established bioinformatic tools and custom scripts. This pipeline needs a combination reference genome and one or more short read (fastq) files.</p>

<h2>Installation</h2>
<h3>Prerequisites</h3>
 <p>To run sppIDer you will need Python 2.7+ with Biopython. Additionally R (http://cran.r-project.org/) and the R packages 'ggplot2' and 'dplyr' are need to parse and plot the information. This pipeline uses existing bioinformatic tools, therefor the following tools are required:</p>
<p>BWA - http://bio-bwa.sourceforge.net/</p>
<p>SAMTOOLS - http://samtools.sourceforge.net/</p>
<p>bedtools genomecov - http://bedtools.readthedocs.io/en/latest/content/tools/genomecov.html</p>

<h3>Initial Usage</h3>
<p>Before running sppIDer all the scripts needed to be downloaded and kept together. Both the combineRefGenomes.py and sppIDer.py scripts need to be edited before the initial run to include the path to these sppIDer scripts as well as the paths to the prerequisites. These are noted as "#EDIT" in the scripts.</p>

<h3>Basic Steps<h3>
<p>combineRefGenomes.py needs to be run first to combine all the desired reference genomes and make the required dictonaries. </p>
<p>sppIDer.py requires the combo ref from above and either one or two fastq files as input. sppIDer.py --h will inform you and basic usage. More details about what these scripts do can be found in sppIDer_manuel.doc and details on the input and output can be found in sppIDerOutput.txt</p>
  
<h3>Many improvments are planned to make sppIDer more useable and will be available soon.</h3>
