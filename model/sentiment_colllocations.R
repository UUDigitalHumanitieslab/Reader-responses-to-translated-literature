library(irr)
library(dplyr)
library(ggplot2)
library(reshape2)

english <- read.csv("../sentiment/English_ratings.csv")
dutch <- read.csv("../sentiment/Dutch_ratings.csv")
french <- read.csv("../sentiment/French_ratings.csv")
german <- read.csv("../sentiment/German_ratings.csv")
portuguese <- read.csv('../sentiment/Portuguese_ratings.csv')
spanish <- read.csv('../sentiment/Spanish_ratings.csv')

kappam.fleiss(english[,2:6], exact=TRUE)
kappam.fleiss(dutch[,2:3], exact=TRUE)
kappam.fleiss(french[,2:3], exact=TRUE)
kappam.fleiss(german[,2:3], exact=TRUE)
kappam.fleiss(portuguese[,2:3], exact=TRUE)
kappam.fleiss(spanish[,2:3], exact=TRUE)

reviews_phn <- read.csv("../sentiment/reviews_PHN.csv")


by_genre <- reviews_phn %>% filter(!grepl('Non', book_genre)) %>%
  mutate(book_genre = ifelse(grepl('Literary', book_genre), "Literary fiction", "Popular fiction")) %>%
  group_by(book_genre, is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))

meltedGenre <- melt(by_genre, id=c('book_genre', 'is_translated'), measure=c('P_mean', 'H_mean', 'N_mean'))

ggplot(meltedGenre, aes(x=book_genre,y=value)) + 
  geom_col(aes(fill=variable), position = 'dodge') +
  labs(title="Book genre", x = "Genre", y = "Average count of positive, negative and hedge terms per review", fill="Term type") + 
  facet_grid(is_translated ~ .)

directions <- reviews_phn %>% filter(is_translated==1) %>%
  mutate(direction = ifelse(
    edition_language=='English', 'nE<E', ifelse(original_language=='English', 'E>nE', 'nE>nE'))) %>%
  group_by(direction) %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))

meltedDirections <- melt(directions, id=c('direction'), measure=c('P_mean', 'H_mean', 'N_mean'))

ggplot(meltedDirections, aes(x=direction,y=value)) + 
  geom_col(aes(fill=variable), position = 'dodge') +
  labs(title="Translation direction", x = "Direction", y = "Average count of positive, negative and hedge terms per review", color = "Translated")

originals <- reviews_phn %>% filter(is_translated==0) %>%
  mutate(edition_language = ifelse(original_language=='English', 'E', 'nE')) %>%
  group_by(edition_language) %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))

meltedOriginals <- melt(originals, id=c('edition_language'), measure=c('P_mean', 'H_mean', 'N_mean'))

ggplot(meltedOriginals, aes(x=edition_language,y=value)) + 
  geom_col(aes(fill=variable), position = 'dodge') +
  labs(title="Originals", x = "Language", y = "Average count of positive, negative and hedge terms per review", color = "Translated")