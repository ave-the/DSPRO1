namespace DCMR.Models;

using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public class OllamaRequest
{
    [JsonPropertyName("model")]
    public string Model { get; set; } = "llama3.2";

    [JsonPropertyName("prompt")]
    public string Prompt { get; set; } = "";

    // Disable streaming so we get a single JSON object back
    [JsonPropertyName("stream")]
    public bool Stream { get; set; } = false;
}

public class OllamaResponse
{
    [JsonPropertyName("model")]
    public string Model { get; set; }

    [JsonPropertyName("response")]
    public string Response { get; set; }

    [JsonPropertyName("done")]
    public bool Done { get; set; }
}

public class OllamaClient
{
    private readonly HttpClient _http;

    public OllamaClient(HttpClient http)
    {
        _http = http;
        _http.BaseAddress = new Uri("http://localhost:11434/");
    }

    public async Task<string> GenerateAsync(string prompt, string model = "llama3.2")
    {
        var req = new OllamaRequest
        {
            Model = model,
            Prompt = prompt,
            Stream = false
        };

        using var response = await _http.PostAsJsonAsync("api/generate", req);

        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();

        var result = JsonSerializer.Deserialize<OllamaResponse>(
            json,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

        return result?.Response ?? string.Empty;
    }
}
