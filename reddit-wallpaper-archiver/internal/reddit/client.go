package reddit

import (
	"net/url"
	"strings"
)

type SavedPost struct {
	ID        string
	Subreddit string
	URL       string
	Title     string
}

func FilterWallpaperPosts(posts []SavedPost) []SavedPost {
	seen := make(map[string]struct{}, len(posts))
	filtered := make([]SavedPost, 0, len(posts))
	for _, post := range posts {
		subreddit := strings.ToLower(post.Subreddit)
		if subreddit != "wallpaper" && subreddit != "wallpapers" {
			continue
		}
		if !isValidURL(post.URL) {
			continue
		}
		if _, exists := seen[post.URL]; exists {
			continue
		}
		seen[post.URL] = struct{}{}
		filtered = append(filtered, post)
	}
	return filtered
}

func isValidURL(raw string) bool {
	parsed, err := url.ParseRequestURI(raw)
	if err != nil {
		return false
	}
	return parsed.Scheme == "http" || parsed.Scheme == "https"
}
