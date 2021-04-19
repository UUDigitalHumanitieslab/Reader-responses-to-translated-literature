library(irr)
library(dplyr)
library(ggplot2)
library(reshape2)

english <- read.csv("../sentiment/English_ratings.csv")
dutch <- read.csv("../sentiment/Dutch_ratings.csv")
french <- read.csv("../sentiment/French_ratings.csv")
german <- read.csv("../sentiment/German_ratings.csv")

kappam.fleiss(english[,3:7], exact=TRUE)
kappam.fleiss(dutch[,3:4], exact=TRUE)
kappam.fleiss(french[,3:4], exact=TRUE)
kappam.fleiss(german[,3:4], exact=TRUE)

reviews_phn <- read.csv("../sentiment/reviews_PHN.csv")
reviews_phn['is_translated'] <- reviews_phn['original_language']==reviews_phn['edition_language']

by_genre <- reviews_phn %>% filter(!grepl('Non', book_genre)) %>%
  mutate(book_genre = ifelse(grepl('Literary', book_genre), "Literary fiction", "Popular fiction")) %>%
  group_by(book_genre, is_translated) %>%
  mutate(is_translated = ifelse(is_translated == FALSE, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))
meltedGenre <- melt(by_genre, id=c('book_genre', 'is_translated'), measure=c('P_mean', 'H_mean', 'N_mean'))

ggplot(meltedGenre, aes(x=book_genre,y=value)) + 
  geom_col(aes(fill=variable), position = 'dodge') +
  labs(title="Book genre", x = "Genre", y = "Average count of positive, negative and hedge terms per review", color = "Translated") + 
  facet_grid(is_translated ~ .)

to_english <- reviews_phn %>% filter(edition_language=='English') %>%
  group_by(is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))

from_english <- reviews_phn %>% filter(original_language=='English') %>%
  group_by(is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))

other <- reviews_phn %>% filter(original_language!='English', edition_language!='English') %>%
  group_by(is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=vars(P, H, N), .funs=c(mean="mean",sum="sum"))

to_english['direction'] <- 'to English'
from_english['direction'] <- 'from English'
other['direction'] <- 'other'

directions <-rbind(to_english, from_english, other)
meltedDirections <- melt(directions, id=c('direction', 'is_translated'), measure=c('P_mean', 'H_mean', 'N_mean'))

ggplot(meltedDirections, aes(x=direction,y=value)) + 
  geom_col(aes(fill=variable), position = 'dodge') +
  labs(title="Translation direction", x = "Direction", y = "Average count of positive, negative and hedge terms per review", color = "Translated") + 
  facet_grid(is_translated ~ .)