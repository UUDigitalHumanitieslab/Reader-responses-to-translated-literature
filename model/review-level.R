library(lme4)
library(ggplot2)
library(reshape2)

# import data

input_path = "../data/goodreads_review_data.csv"
data = read.csv(input_path)

# filters

min_review_length = function(data, min_length = 1) {
  subset(data, data$words >= min_length)
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
  
  res
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
  
  res
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
  
  res
}


# rating vs mentioning of translation

ratings = 1:5
rating_data = data.frame(
  rating = ratings,
  n_reviews = sapply(ratings, function(rating) {nrow(subset(data, data$rating_no == rating))}),
  p_mention_translation = sapply(ratings, function(rating) {count_translation_mentions(subset(data, data$rating_no == rating))})
)

p = ggplot(data = rating_data) +
  geom_line(aes(x = rating, y = p_mention_translation))
p
  