export interface MovieData {
  movie_id: number,
  movie_title: string,
  rating: number | undefined,
  tag: string | undefined,
  timestamp: number
}

export interface ResponseData {
  ratings : MovieData[],
  ratings_count: number,
  tags: MovieData[],
  tags_count: number,
  user_id: number,
  username: string
}
