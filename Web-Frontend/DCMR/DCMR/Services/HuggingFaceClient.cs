namespace DCMR.Services;

using System.Text.Json;
using System.Net.Http.Headers;
using System.Text;
using DCMR.Models;


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
public async Task<string> GenerateImageAsync(List<Ingredient> ingredients)
    {
        return await GetRecipeAsync(ingredients);
    }
    public async Task<string> GetRecipeAsync(List<Ingredient> ingredients)
    {
        var prompt = "A high quality food photo of a dish made with: " +
                     string.Join(", ", ingredients.Select(i => i.Name)) +
                     ". Highly detailed, professional lighting, 8k resolution.";

        var request = new
        {
            inputs = prompt,
            parameters = new
            {
                width = 512,
                height = 512,
                num_inference_steps = 50
            }
        };

        var response = await _client.PostAsJsonAsync(
            "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
            request
        );

        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();
        return json;
    }
}