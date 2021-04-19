library(irr)

english <- read.csv("../sentiment/English_ratings.csv")
dutch <- read.csv("../sentiment/Dutch_ratings.csv")
french <- read.csv("../sentiment/French_ratings.csv")
german <- read.csv("../sentiment/German_ratings.csv")

kappam.fleiss(english[,3:7], exact=TRUE)
kappam.fleiss(dutch[,3:4], exact=TRUE)
kappam.fleiss(french[,3:4], exact=TRUE)
kappam.fleiss(german[,3:4], exact=TRUE)
