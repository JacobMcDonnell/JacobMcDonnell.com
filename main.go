package main

import (
	"fmt"
	"github.com/gomarkdown/markdown"
	"github.com/gomarkdown/markdown/html"
	"github.com/gomarkdown/markdown/parser"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"slices"
)

func GetHome(w http.ResponseWriter, r *http.Request) {
	log.Println("Request for:", r.URL.String())

	if r.URL.String() != "/" {
		ErrorPage(w, "Page Not Found.", 404)
		return
	}

	t := template.Must(template.ParseFiles("templates/template.html"))

	html, err := MarkdownToHTML("static/home.md")
	if err != nil {
		ErrorPage(w, "Internal Server Error", 500)
	} else {
		t.Execute(w, template.HTML(html))
	}
}

func GetFiles(w http.ResponseWriter, r *http.Request) {
	log.Println("Request for:", r.URL.String())
	url := fmt.Sprintf("static%s", r.URL.String())

	allowed := []string{
		"static/rss.xml",
		"static/card",
		"static/css/main.css",
		"static/logos/FirstInitialLogo.svg",
		"static/logos/FullNameLogo.svg",
		"static/logos/favicon.png",
		"static/logos/favicon.svg",
		"static/logos/favicon16.png",
		"static/logos/favicon32.png",
		"static/robots.txt",
	}

	if slices.Contains(allowed, url) {
		http.ServeFile(w, r, url)
	} else {
		ErrorPage(w, "Page Not Found.", 404)
	}
}

func MarkdownToHTML(path string) (string, error) {
	extensions := parser.CommonExtensions | parser.AutoHeadingIDs | parser.NoEmptyLineBeforeBlock
	p := parser.NewWithExtensions(extensions)

	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()

	md, err := io.ReadAll(f)
	if err != nil {
		return "", err
	}

	doc := p.Parse(md)

	htmlFlags := html.CommonFlags | html.HrefTargetBlank
	opts := html.RendererOptions{Flags: htmlFlags}
	renderer := html.NewRenderer(opts)

	return string(markdown.Render(doc, renderer)), nil
}

func ErrorPage(w http.ResponseWriter, message string, code int) {
	log.Println(code, message)
	t := template.Must(template.ParseFiles("templates/error.html"))
	t.Execute(w, struct {
		Code    int
		Message string
	}{
		Code:    code,
		Message: message,
	})
}

func main() {
	http.HandleFunc("/robots.txt", GetFiles)
	http.HandleFunc("/rss.xml", GetFiles)
	http.HandleFunc("/card", GetFiles)
	http.HandleFunc("/css/", GetFiles)
	http.HandleFunc("/logos/", GetFiles)
	http.HandleFunc("/", GetHome)
	log.Fatal(http.ListenAndServe(":8000", nil))
}
