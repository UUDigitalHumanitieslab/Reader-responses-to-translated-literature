library(lme4)
library(ggplot2)
library(reshape2)
library(dplyr)

# import data

input_path = "../data/goodreads_review_data.csv"
data = read.csv(input_path)

# filters

min_review_length = function(data, min_length = 1) {
  subset(data, data$words >= min_length)
}

only_translated = function(data) {
  subset(data, data$is_translated)
}

# counting functions

count_translation_mentions = function(data, absolute = FALSE) {
  values = subset(data$mentions_translation, !is.na(data$mentions_translation))
  if (absolute) {
    return(sum(values))
  }
  else {
    return(sum(values)/length(values))
  }
}

translation_frequency = function(data) {
  all_data = subset(data, data$words >= 10)
  mention_data = subset(all_data, as.logical(all_data$mentions_translation))
  total_mentions = sum(mention_data$mention_count) #to do: add column with count instead of bool
  total_words = sum(all_data$words)
  
  total_mentions / total_words
}

count_reviews = function(data) {
  nrow(data)
}

count_titles = function(data) {
  length(unique(data$book_title))
}

#quick overview of how many reviews are from translated books and how many mention translation

table(data[,c("mentions_translation", "is_translated")])

# full overview of data per language

original_languages = unique(data$original_language[as.character(data$original_language) != ""])
edition_languages = unique(data$edition_language[as.character(data$edition_language) != ""])

full_table = function(data) {
  res = data.frame()
  
  for (og_lang in original_languages) {
    for (ed_lang in edition_languages) {
      subdata = subset(data, 
                       data$original_language == og_lang & data$edition_language == ed_lang)
      new_row = data.frame(original_language = og_lang, 
                           edition_language = ed_lang,
                           is_translated = as.character(og_lang) != as.character(ed_lang),
                           n_titles = count_titles(subdata),
                           n_reviews = count_reviews(subdata),
                           n_mention_translation = count_translation_mentions(subdata, absolute=TRUE),
                           p_mention_translation = count_translation_mentions(subdata)
                           )
      res = rbind(res, new_row)
    }
  }
  
  return(res)
}

oglang_table = function(data) {
  res = data.frame()
  
  for (og_lang in original_languages) {
      subdata = subset(data, 
                       data$original_language == og_lang & as.character(data$edition_language) != as.character(data$original_language))
      new_row = data.frame(original_language = og_lang, 
                           n_titles = count_titles(subdata),
                           n_reviews = count_reviews(subdata),
                           n_mention_translation = count_translation_mentions(subdata, absolute=TRUE),
                           p_mention_translation = count_translation_mentions(subdata)
      )
      res = rbind(res, new_row)
  }
  
  return(res)
}

edlang_table = function(data) {
  res = data.frame()
  
  for (ed_lang in edition_languages) {
    subdata = subset(data, 
                     data$edition_language == ed_lang & as.character(data$edition_language) != as.character(data$original_language))
    new_row = data.frame(edition_language = ed_lang, 
                         n_titles = count_titles(subdata),
                         n_reviews = count_reviews(subdata),
                         n_mention_translation = count_translation_mentions(subdata, absolute=TRUE),
                         p_mention_translation = count_translation_mentions(subdata)
    )
    res = rbind(res, new_row)
  }
  
  return(res)
}

editions <- edlang_table(table)


# rating vs mentioning of translation


ratings = 1:5

rating_data = rbind(
  data.frame(
    is_translated = rep("translated", length(ratings)),
    rating = ratings,
    n_reviews = sapply(ratings, 
                       function(r) {
                         nrow(subset(data, data$rating_no == r & data$is_translated))
                       }),
    translation_freq = sapply(ratings,
                                   function (r) {
                                     translation_frequency(subset(data, data$rating_no == r & data$is_translated))
                                   })
    ),
  data.frame(
    is_translated = rep("not translated", length(ratings)),
    rating = ratings,
    n_reviews = sapply(ratings, 
                       function(r) {
                         nrow(subset(data, data$rating_no == r & ! data$is_translated))
                       }),
    translation_freq = sapply(ratings,
                                   function (r) {
                                     translation_frequency(subset(data, data$rating_no == r & ! data$is_translated))
                                   })
  )
)
rating_data

#plot

ggplot(data = rating_data) +
  geom_line(aes(x = rating, y = translation_freq, color = is_translated), size = 1) +
  ylim(c(0, NA)) +
  labs(x = "rating", y = "frequency of 'translation'", color = "edition")

#model

mention_model = glm(mentions_translation ~ rating_no * is_translated, data, family = binomial)
summary(mention_model)

rating_data_test <- data %>% filter(!is.na(mentions_translation), !is.na(rating_no), words>10) %>%
  group_by(rating_no, is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=c('n', 'mention_count'), .funs=c(mean="mean",sum="sum")) %>%
  select(-c('n_sum')) %>% rename(n=n_mean)

ggplot(data = rating_data_test) +
  geom_line(aes(x = rating_no, y = mention_count_mean, color = is_translated), size = 1) +
  ylim(c(0, NA)) +
  labs(title="Ungrouped reviews", x = "Goodreads rating", y = "Average count of translation lemma per review", color = "Translated")


by_edition <- data %>% filter(!is.na(mentions_translation), !is.na(rating_no), words>10) %>%
              group_by(edition_language, rating_no, is_translated) %>%
              mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
              add_tally() %>%
              summarise_at(.vars=c('n', 'mention_count'), .funs=c(mean="mean",sum="sum")) %>%
              select(-c('n_sum')) %>% rename(n=n_mean)

ggplot(data=by_edition) + 
  geom_line(aes(x=rating_no, y=mention_count_mean, color=is_translated), size=1) +
  ylim(c(0, NA)) +
  labs(title="Edition language", x = "Goodreads rating", y = "Average count of translation lemma per review", color = "Translated") + 
  facet_grid(edition_language ~ .)

by_original <- data %>% filter(!is.na(mentions_translation), !is.na(rating_no), words>10) %>%
              group_by(original_language, rating_no, is_translated) %>%
              mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
              add_tally() %>%
              summarise_at(.vars=c('n', 'mention_count'), .funs=c(mean="mean",sum="sum")) %>%
              select(-c('n_sum')) %>% rename(n=n_mean)

ggplot(data=by_original) + 
  geom_line(aes(x=rating_no, y=mention_count_mean, color=is_translated), size=1) +
  ylim(c(0, NA)) +
  labs(title="Original language", x = "Goodreads rating", y = "Average count of translation lemma per review", color = "Translated") +  
  facet_grid(original_language ~ .)

by_genre <- data %>% filter(!is.na(mentions_translation), !is.na(rating_no), !grepl('Non', book_genre)) %>%
              mutate(book_genre = ifelse(grepl('Literary', book_genre), "Literary fiction", "Popular fiction")) %>%
              group_by(book_genre, rating_no, is_translated) %>%
              mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
              add_tally() %>%
              summarise_at(.vars=c('n', 'mention_count'), .funs=c(mean="mean",sum="sum")) %>%
              select(-c('n_sum')) %>% rename(n=n_mean)

ggplot(data=by_genre) + 
  geom_line(aes(x=rating_no, y=mention_count_mean, color=is_translated), size=1) +
  ylim(c(0, NA)) +
  labs(title="Book genre", x = "Goodreads rating", y = "Average count of translation lemma per review", color = "Translated") + 
  facet_grid(book_genre ~ .)

levels(by_genre$is_translated)

numbers <- data %>% filter(!is.na(mentions_translation), !is.na(is_translated)) %>%
  group_by(mentions_translation, is_translated) %>%
  tally()

from_english <- data %>% filter(!is.na(mentions_translation), !is.na(rating_no), grepl('English', original_language)) %>%
  group_by(rating_no, is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=c('n', 'mention_count'), .funs=c(mean="mean",sum="sum")) %>%
  select(-c('n_sum')) %>% rename(n=n_mean)

ggplot(data=from_english) + 
  geom_line(aes(x=rating_no, y=mention_count_mean, color=is_translated), size=1) +
  ylim(c(0, NA)) +
  labs(title="Books originally published in English", x = "Goodreads rating", y = "Average count of translation lemma per review", color = "Translated")

to_english <- data %>% filter(!is.na(mentions_translation), !is.na(rating_no), grepl('English', edition_language)) %>%
  group_by(rating_no, is_translated) %>%
  mutate(is_translated = ifelse(is_translated == 0, "not translated", "translated")) %>%
  add_tally() %>%
  summarise_at(.vars=c('n', 'mention_count'), .funs=c(mean="mean",sum="sum")) %>%
  select(-c('n_sum')) %>% rename(n=n_mean)

ggplot(data=to_english) + 
  geom_line(aes(x=rating_no, y=mention_count_mean, color=is_translated), size=1) +
  ylim(c(0, NA)) +
  labs(title="Books published in English", x = "Goodreads rating", y = "Average count of translation lemma per review", color = "Translated")
