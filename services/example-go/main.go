package main

import (
	"flag"
	"fmt"
	"html/template"
	"log"
	"net"
	"net/http"
	"os"
	"runtime"
	"sort"
	"strings"
	"time"
)

var startTime time.Time

func uptime() time.Duration {
	return time.Since(startTime)
}

func init() {
	startTime = time.Now()
}

var indexTemplate = template.Must(template.New("Index").Parse(`<!DOCTYPE html>
<html>
<head>
<title>example-go</title>
<style>
body {
	font-family: monospace;
	color: #555;
	background: #e6edf4;
	padding: 1.25rem;
	margin: 0;
}
table {
	background: #fff;
	border: .0625rem solid #c4cdda;
	border-radius: 0 0 .25rem .25rem;
	border-spacing: 0;
	margin-bottom: 1.25rem;
	padding: .75rem 1.25rem;
	text-align: left;
	white-space: pre;
}
table > caption {
	background: #f1f6fb;
	text-align: left;
	font-weight: bold;
	padding: .75rem 1.25rem;
	border: .0625rem solid #c4cdda;
	border-radius: .25rem .25rem 0 0;
	border-bottom: 0;
}
table td, table th {
	padding: .25rem;
}
table > tbody > tr:hover {
	background: #f1f6fb;
}
</style>
</head>
<body>
	<table>
		<caption>Actions</caption>
		<tr>
			<td><a href="400-empty-json-property-name.json">return a 400 with a JSON document that has an empty JSON property name</a></td>
		</tr>
	</table>
	<table>
		<caption>Properties</caption>
		<tr><th>Pid</th><td>{{.Pid}}</td></tr>
		<tr><th>Uid</th><td>{{.Uid}}</td></tr>
		<tr><th>Gid</th><td>{{.Gid}}</td></tr>
		<tr><th>Request</th><td>{{.Request}}</td></tr>
		<tr><th>Client Address</th><td>{{.ClientAddress}}</td></tr>
		<tr><th>Server Address</th><td>{{.ServerAddress}}</td></tr>
		<tr><th>Hostname</th><td>{{.Hostname}}</td></tr>
		<tr><th>Os</th><td>{{.Os}}</td></tr>
		<tr><th>Architecture</th><td>{{.Architecture}}</td></tr>
		<tr><th>Runtime</th><td>{{.Runtime}}</td></tr>
		<tr><th>Uptime</th><td>{{.Uptime}}</td></tr>
	</table>
	<table>
		<caption>Request Headers</caption>
		{{- range .RequestHeaders}}
		<tr>
			<th>{{.Name}}</th>
			<td>{{.Value}}</td>
		</tr>
		{{- end}}
	</table>
	<table>
		<caption>Environment Variables</caption>
		{{- range .Environment}}
		<tr>
			<th>{{.Name}}</th>
			<td>{{.Value}}</td>
		</tr>
		{{- end}}
	</table>
</body>
</html>
`))

var exampleValidationErrorJSON = `{
	"Title": "One or more validation errors occurred.",
	"Errors": {
	  "": [
		"The supplied value is invalid."
	  ],
	  "name": [
		"'name' cannot be null."
	  ]
	},
	"Type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
	"Status": 400,
	"Extensions": {
	  "traceId": "00-f443e487a4998c41a6fd6fe88bae644e-5b7253de08ed474f-01"
	}
}`

type nameValuePair struct {
	Name  string
	Value string
}

type indexData struct {
	Pid            int
	Uid            int
	Gid            int
	Request        string
	RequestHeaders []nameValuePair
	ClientAddress  string
	ServerAddress  string
	Hostname       string
	Os             string
	Architecture   string
	Runtime        string
	Uptime         string
	Environment    []nameValuePair
}

type nameValuePairs []nameValuePair

func (a nameValuePairs) Len() int           { return len(a) }
func (a nameValuePairs) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a nameValuePairs) Less(i, j int) bool { return a[i].Name < a[j].Name }

type wrappedWriter struct {
	http.ResponseWriter
	statusCode int
}

func (w *wrappedWriter) WriteHeader(statusCode int) {
	w.ResponseWriter.WriteHeader(statusCode)
	w.statusCode = statusCode
}

func accessLog(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		wrapped := &wrappedWriter{
			ResponseWriter: w,
			statusCode:     http.StatusOK,
		}
		next.ServeHTTP(wrapped, r)
		log.Printf("%s %s%s %d %s", r.Method, r.Host, r.URL, wrapped.statusCode, time.Since(start))
	})
}

func main() {
	log.SetFlags(0)

	var listenAddress = flag.String("listen", ":8000", "Listen address.")

	flag.Parse()

	if flag.NArg() != 0 {
		flag.Usage()
		log.Fatalf("\nERROR You MUST NOT pass any positional arguments")
	}

	router := http.NewServeMux()

	router.HandleFunc("GET /400-empty-json-property-name.json", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(400)
		w.Write([]byte(exampleValidationErrorJSON))
	})

	router.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.Error(w, "Not Found", http.StatusNotFound)
			return
		}

		hostname, err := os.Hostname()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "text/html")

		environment := make([]nameValuePair, 0)
		for _, v := range os.Environ() {
			parts := strings.SplitN(v, "=", 2)
			name := parts[0]
			value := parts[1]
			switch name {
			case "PATH":
				fallthrough
			case "XDG_DATA_DIRS":
				fallthrough
			case "XDG_CONFIG_DIRS":
				value = strings.Join(
					strings.Split(value, string(os.PathListSeparator)),
					"\n")
			}
			environment = append(environment, nameValuePair{name, value})
		}
		sort.Sort(nameValuePairs(environment))

		requestHeaders := make([]nameValuePair, 0)
		for k, values := range r.Header {
			for _, v := range values {
				requestHeaders = append(requestHeaders, nameValuePair{k, v})
			}
		}
		sort.Sort(nameValuePairs(requestHeaders))

		err = indexTemplate.ExecuteTemplate(w, "Index", indexData{
			Pid:            os.Getpid(),
			Uid:            os.Getuid(),
			Gid:            os.Getgid(),
			Request:        fmt.Sprintf("%s %s%s", r.Method, r.Host, r.URL),
			RequestHeaders: requestHeaders,
			ClientAddress:  r.RemoteAddr,
			ServerAddress:  r.Context().Value(http.LocalAddrContextKey).(net.Addr).String(),
			Hostname:       hostname,
			Os:             runtime.GOOS,
			Architecture:   runtime.GOARCH,
			Runtime:        runtime.Version(),
			Uptime:         uptime().String(),
			Environment:    environment,
		})
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	})

	server := http.Server{
		Addr:    *listenAddress,
		Handler: accessLog(router),
	}

	log.Printf("Listening at http://%s", *listenAddress)

	err := server.ListenAndServe()
	if err != nil {
		log.Fatalf("Failed to ListenAndServe: %v", err)
	}
}
