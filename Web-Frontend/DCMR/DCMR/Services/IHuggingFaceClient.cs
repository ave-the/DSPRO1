namespace DCMR.Services;

public interface IHuggingFaceClient
{
    Task<string> QueryAsync(string prompt);
}