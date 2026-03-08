namespace ConsoleApp11
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("To what range sum?");
            int range = Convert.ToInt32(Console.ReadLine());

            Console.WriteLine("From n = ?");
            int n = Convert.ToInt32(Console.ReadLine());

            if (n > range)
            {
                Console.WriteLine("n must be smaller than range.");
                return;
            }

            int sumToRange = range * (range + 1) / 2;
            int sumToBeforeN = (n - 1) * n / 2;

            int result = sumToRange - sumToBeforeN;

            Console.WriteLine("Result: " + result);
        }
    }
}
