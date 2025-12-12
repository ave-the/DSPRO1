using DCMR.Models;

namespace DCMR.Services;

public interface IHuggingFaceClient
{
    Task<string> QueryAsync(string prompt);

    Task<string> GetRecipeAsync(List<Ingredient> ingredients);
}