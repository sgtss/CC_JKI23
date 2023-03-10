#!/usr/bin/env R

# setting up default repo source, just in case not setup in .Rprofile
options(repos = list(CRAN="http://cran.rstudio.com/"))

# Packages to be used
packages <- c("igraph",
            "ggplot2",
            "gridExtra",
            "label.switching",
            "tidyr",
            "remotes",
            "colourpicker",
            "DT",
            "highcharter",
            "htmlwidgets",
            "magrittr",
            "markdown",
            "RColorBrewer",
            "shiny",
            "shinyAce",
            "shinyBS",
            "shinythemes",
            "shinyWidgets",
            "viridisLite",
            "writexl")

#install all packages that are not already installed
install.packages(setdiff(packages, rownames(installed.packages())))

# Needs devtools; very piniky; rather use remotes
#install_github("royfrancis/pophelper")

# install pophelper package from GitHub
remotes::install_github('royfrancis/pophelper')