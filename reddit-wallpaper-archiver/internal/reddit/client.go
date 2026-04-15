package reddit

import "strings"

type SavedPost struct {
	ID        string
	Subreddit string
	URL       string
	Title     string
}

func FilterWallpaperPosts(posts []SavedPost) []SavedPost {
	filtered := make([]SavedPost, 0, len(posts))
	for _, post := range posts {
		subreddit := strings.ToLower(post.Subreddit)
		if subreddit == "wallpaper" || subreddit == "wallpapers" {
			filtered = append(filtered, post)
		}
	}
	return filtered
}
