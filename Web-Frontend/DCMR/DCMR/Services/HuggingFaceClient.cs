namespace DCMR.Services;

using System.Text.Json;
using System.Net.Http.Headers;
using System.Text;


public class HuggingFaceClient : IHuggingFaceClient
{
    private readonly HttpClient _client;

    public HuggingFaceClient(IHttpClientFactory httpClientFactory)
    {
        _client = httpClientFactory.CreateClient();
        var apiKey = Environment.GetEnvironmentVariable("HF_API_KEY");
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
    }


    public async Task<string> QueryAsync(string prompt)
    {
        var request = new
        {
            inputs = prompt,
            parameters = new
            {
                max_new_tokens = 300,
                temperature = 0.7
            }
        };


        var response = await _client.PostAsJsonAsync(
            "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct",
            request
        );


        response.EnsureSuccessStatusCode();


        var json = await response.Content.ReadAsStringAsync();
        return json;
    }
}