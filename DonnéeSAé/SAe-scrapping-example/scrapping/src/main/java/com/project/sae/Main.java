package com.project.sae ;


import java.io.FileWriter;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import com.opencsv.CSVWriter;

public class Main {

    public static void main(String[] args) {

        // create HtttpClient instance
        HttpClient client = HttpClient.newHttpClient();

        // build a HttpRequest
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://www.scrapingcourse.com/ecommerce/"))
            .build();

        // send asynchronous GET request and handle response.
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            // extract body as string
            .thenApply(HttpResponse::body)

            // retrieve extracted body
            .thenAccept(htmlContent -> {
            // parse the HTML content using Jsoup
            Document doc = Jsoup.parse(htmlContent);

            // select all product elements
            Elements productElements = doc.select(".product");

            // initialize CSV writer
            try (CSVWriter csvWriter = new CSVWriter(new FileWriter("products.csv"))) {
                // write header
                csvWriter.writeNext(new String[]{"Product Title", "Image URL", "Link"});

                // iterate through each product
                for (Element productElement : productElements) {
                    // retrieve the product title
                    String productTitle = productElement.select("h2").text();
                    // retrieve the image URL
                    String imageUrl = productElement.select("img[src]").attr("src");
                    // retrieve the link
                    String link = productElement.select("a[href]").attr("href");
                    // write data to CSV
                    csvWriter.writeNext(new String[]{productTitle, imageUrl, link});
                }
                System.out.println("Data successfully exported to CSV");
            } catch (IOException e) {
                e.printStackTrace();
            }

        }).join();
    }
}
