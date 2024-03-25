library(dplyr)

input_path = "../data/goodreads_review_data.csv"
data = read.csv(input_path)

data_words <- data %>% filter(cleaned_words>0)

orig <- data_words %>% group_by(original_language)
orig_reviews <- orig %>% tally()
orig_words <- orig %>% summarise_at(.vars=vars(words), .funs=c(sum="sum"))


edition <- data_words %>% group_by(edition_language)
edit_reviews <- edition %>% tally()
edit_words <- edition %>% summarise_at(.vars=vars(words), .funs=c(sum="sum"))

review <- data_words %>% group_by(language)
review_reviews <- review %>% tally()
review_words <- review %>% summarise_at(.vars=vars(words), .funs=c(sum="sum"))

genre <- data_words %>% group_by(book_genre)
genre_reviews <- genre %>% tally()
genre_words <- genre %>% summarise_at(.vars=vars(words), .funs=c(sum="sum"))
