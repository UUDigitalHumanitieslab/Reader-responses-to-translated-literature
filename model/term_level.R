library(lme4)
library(ggplot2)
library(reshape2)

# import data

input_path = "../data/goodreads_formatted.csv"
data = read.csv(input_path)

# PREPROCESSING

#simplified genre definition (just literary fiction and popular fiction)

simple_genre = function(genre) {
  if (genre == "Literary fiction") {
    return(genre)
  }
  
  if (startsWith(genre, "Popular fiction")) {
    return("Popular fiction")
  }
  
  return (NA)
}


simple_genres = as.factor(sapply(as.character(data[, "book_genre"]), simple_genre))
data$book_simple_genre = simple_genres


#format with melted term types - useful for testing effect on which terms are used more

melted_term_data = melt(data, 
                        id.vars = c("original_language", "edition_language", "language", "age_category", "book_genre", "book_simple_genre", "rating_no"), 
                        measure.vars = c("positive", "negative", "hedge"), 
                        variable.name = "term_type", value.name = "count")


# correct for main effect of term type and rating
model_term = lm(count ~ term_type + rating_no + term_type * rating_no, data = melted_term_data, na.action = na.exclude)
melted_term_data$corrected_count = residuals(model_term)

# LINEAR MODELS


#terms and rating

model_rating = lm(rating_no ~ negative + positive + hedge, data = data)
summary(model_rating)

#effect of (simplified) genre on rating

model_rating_genre = lm(rating_no ~ book_simple_genre, data = data)
summary(model_rating_genre)

#interaction effect between simple genre and term frequency

model_genre_term = lm(corrected_count ~ book_simple_genre * term_type, data = melted_term_data)
summary(model_genre_term)

# PLOTS

# plot terms vs rating

values_per_rating = function(rating, value, data) {
  fdata = subset(data, rating_no == rating)
  fdata[, value]
}

ratings = 1:5

data_per_rating = data.frame(
  rating = ratings,
  hedge_mean = sapply(ratings, function(r) {mean(values_per_rating(r, "hedge", data))}),
  pos_mean = sapply(ratings, function(r) {mean(values_per_rating(r, "positive", data))}),
  neg_mean = sapply(ratings, function(r) {mean(values_per_rating(r, "negative", data))})
)

p = ggplot(data = data_per_rating) +
  geom_line(aes(rating, neg_mean, color = "negative"), size=1) +
  geom_line(aes(rating, pos_mean, color = "positive"), size=1) +
  geom_line(aes(rating, hedge_mean, color = "hedge"), size=1) +
  ylab("average frequency") +
  labs(color = "term type") +
  scale_colour_manual(values= c(
    "positive" = "#00cc66", 
    "hedge" = "#3399ff", 
    "negative" = "#ff3333"
    ))

p 

# genre and term

genres = levels(simple_genres)

mean_per_genre_and_term = function(genre, term) {
  genre_data = subset(melted_term_data, melted_term_data$book_simple_genre == genre & melted_term_data$term_type == term)
  mean(genre_data$corrected_count, na.rm = TRUE)
}


results_per_term = function(term) {
  values = sapply(genres, function(g) {mean_per_genre_and_term(g, term)})
  
  values
}

results_per_genre = data.frame(
  genre = genres,
  positive = results_per_term("positive"),
  negative = results_per_term("negative"),
  hedge = results_per_term("hedge")
)


melted_results_per_genre = melt(results_per_genre, id=c("genre"))

p = ggplot(data = melted_results_per_genre) +
  geom_line(aes(x = variable, y = value, group = genre, color = genre), size =1) +
  theme(legend.position ="top") +
  labs(y="frequency", x="term type")


p

# plot rating per genre



rating_per_genre = function(genre) {
  genre_data = subset(data, data$book_simple_genre == genre)
  df = data.frame(table(genre_data$rating_no))
  names(df) = c("rating", "frequency")
  df$genre = rep(genre, nrow(df))
  
  df
}

rbind(rating_per_genre(genres[1]), rating_per_genre(genres[2]))

