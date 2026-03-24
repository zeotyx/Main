using System;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using NCalc;

namespace calculator
{
    public partial class MainWindow : Window
    {
        private StringBuilder calculation = new StringBuilder();

        public MainWindow()
        {
            InitializeComponent();
            this.PreviewKeyDown += MainWindow_PreviewKeyDown;
            DisplayTextBlock.Text = "0";
        }

        // -------------------- NUMBER BUTTONS --------------------
        private void NumberButton_Click(object sender, RoutedEventArgs e)
        {
            string number = (sender as Button).Content.ToString();
            AppendNumber(number);
        }

        private void AppendNumber(string number)
        {
            calculation.Append(number);
            DisplayTextBlock.Text = calculation.ToString();
        }

        private void OperatorButton_Click(object sender, RoutedEventArgs e)
        {
            string op = (sender as Button).Content.ToString();
            AppendOperator(op);
        }

        private void AppendOperator(string op)
        {
            if (calculation.Length == 0 && op != "(") return;

            char lastChar = calculation.Length > 0 ? calculation[^1] : ' ';
            if ("+-*/^".Contains(lastChar) && "+-*/^".Contains(op)) return;

            calculation.Append(op);
            DisplayTextBlock.Text = calculation.ToString();
        }

       
        private void FunctionButton_Click(object sender, RoutedEventArgs e)
        {
            string func = (sender as Button).Content.ToString();
            if (func == "√") func = "sqrt";

            if (calculation.Length > 0 && (char.IsDigit(calculation[^1]) || calculation[^1] == ')'))
                calculation.Append("*");

            calculation.Append(func + "(");
            DisplayTextBlock.Text = calculation.ToString();
        }

       
        private void ButtonEquals_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                string exprStr = InsertImplicitMultiplication(calculation.ToString());
                NCalc.Expression expr = new NCalc.Expression(exprStr);

                expr.EvaluateFunction += delegate (string name, FunctionArgs args)
                {
                    double arg = Convert.ToDouble(args.Parameters[0].Evaluate());
                    switch (name)
                    {
                        case "sin": args.Result = Math.Sin(ToRadians(arg)); break;
                        case "cos": args.Result = Math.Cos(ToRadians(arg)); break;
                        case "tan": args.Result = Math.Tan(ToRadians(arg)); break;
                        case "sqrt": args.Result = Math.Sqrt(arg); break;
                        case "log": args.Result = Math.Log10(arg); break;
                        case "ln": args.Result = Math.Log(arg); break;
                    }
                };

                var result = expr.Evaluate();
                calculation.Clear();
                calculation.Append(result.ToString());
                DisplayTextBlock.Text = result.ToString();
            }
            catch
            {
                DisplayTextBlock.Text = "Error";
                calculation.Clear();
            }
        }

       
        private void ButtonClear_Click(object sender, RoutedEventArgs e)
        {
            calculation.Clear();
            DisplayTextBlock.Text = "0";
        }

        
        private void ButtonBackspace_Click(object sender, RoutedEventArgs e)
        {
            if (calculation.Length > 0)
            {
                calculation.Remove(calculation.Length - 1, 1);
                DisplayTextBlock.Text = calculation.Length > 0 ? calculation.ToString() : "0";
            }
        }

       
        private string InsertImplicitMultiplication(string expr)
        {
            StringBuilder newExpr = new StringBuilder();
            for (int i = 0; i < expr.Length; i++)
            {
                newExpr.Append(expr[i]);
                if (i < expr.Length - 1)
                {
                    char current = expr[i];
                    char next = expr[i + 1];
                    if ((char.IsDigit(current) || current == ')') && (char.IsLetter(next) || next == '('))
                        newExpr.Append("*");
                }
            }
            return newExpr.ToString();
        }

        private double ToRadians(double degrees) => degrees * Math.PI / 180;

      
        private void MainWindow_PreviewKeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key >= Key.D0 && e.Key <= Key.D9) AppendNumber((e.Key - Key.D0).ToString());
            else if (e.Key >= Key.NumPad0 && e.Key <= Key.NumPad9) AppendNumber((e.Key - Key.NumPad0).ToString());
            else if (e.Key == Key.Add) AppendOperator("+");
            else if (e.Key == Key.Subtract) AppendOperator("-");
            else if (e.Key == Key.Multiply) AppendOperator("*");
            else if (e.Key == Key.Divide) AppendOperator("/");
            else if (e.Key == Key.OemPeriod || e.Key == Key.Decimal) AppendNumber(".");
            else if (e.Key == Key.Enter) ButtonEquals_Click(null, null);
            else if (e.Key == Key.Back) ButtonBackspace_Click(null, null);
            else if (e.Key == Key.OemOpenBrackets) AppendOperator("(");
            else if (e.Key == Key.OemCloseBrackets) AppendOperator(")");
        }
    }
}



<Window x:Class="calculator.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Calculator" Height="650" Width="380"
        Background="#1C1C1C">

    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>

        <!-- Display -->
        <Border Grid.Row="0" CornerRadius="25" Background="#2A2A2A" Padding="20">
            <TextBlock x:Name="DisplayTextBlock"
                       FontSize="36"
                       Foreground="White"
                       TextAlignment="Right"
                       VerticalAlignment="Center"
                       TextWrapping="Wrap"/>
        </Border>

        <!-- Buttons -->
        <UniformGrid Grid.Row="1" Rows="7" Columns="4" Margin="0,20,0,0">
            <UniformGrid.Resources>
                <Style TargetType="Button">
                    <Setter Property="FontSize" Value="20"/>
                    <Setter Property="Margin" Value="5"/>
                    <Setter Property="Foreground" Value="White"/>
                    <Setter Property="BorderThickness" Value="0"/>
                    <Setter Property="Height" Value="60"/>
                    <Setter Property="Template">
                        <Setter.Value>
                            <ControlTemplate TargetType="Button">
                                <Border x:Name="border" CornerRadius="18" Background="{TemplateBinding Background}">
                                    <ContentPresenter HorizontalAlignment="Center" VerticalAlignment="Center"/>
                                </Border>
                                <ControlTemplate.Triggers>
                                    <Trigger Property="IsMouseOver" Value="True">
                                        <Setter TargetName="border" Property="RenderTransform">
                                            <Setter.Value>
                                                <ScaleTransform ScaleX="1.05" ScaleY="1.05"/>
                                            </Setter.Value>
                                        </Setter>
                                        <Setter TargetName="border" Property="Effect">
                                            <Setter.Value>
                                                <DropShadowEffect Color="Orange" BlurRadius="18" ShadowDepth="0"/>
                                            </Setter.Value>
                                        </Setter>
                                    </Trigger>
                                    <Trigger Property="IsPressed" Value="True">
                                        <Setter TargetName="border" Property="RenderTransform">
                                            <Setter.Value>
                                                <ScaleTransform ScaleX="0.95" ScaleY="0.95"/>
                                            </Setter.Value>
                                        </Setter>
                                        <Setter TargetName="border" Property="Effect">
                                            <Setter.Value>
                                                <DropShadowEffect Color="Orange" BlurRadius="28" ShadowDepth="0"/>
                                            </Setter.Value>
                                        </Setter>
                                    </Trigger>
                                </ControlTemplate.Triggers>
                            </ControlTemplate>
                        </Setter.Value>
                    </Setter>
                </Style>
            </UniformGrid.Resources>

            <!-- Row 1: Trig + divide -->
            <Button Content="sin" Background="#FF9500" Click="FunctionButton_Click"/>
            <Button Content="cos" Background="#FF9500" Click="FunctionButton_Click"/>
            <Button Content="tan" Background="#FF9500" Click="FunctionButton_Click"/>
            <Button Content="/" Background="#FF9500" Click="OperatorButton_Click"/>

            <!-- Row 2: sqrt, ln, log, power -->
            <Button Content="√" Background="#FF9500" Click="FunctionButton_Click"/>
            <Button Content="ln" Background="#FF9500" Click="FunctionButton_Click"/>
            <Button Content="log" Background="#FF9500" Click="FunctionButton_Click"/>
            <Button Content="^" Background="#FF9500" Click="OperatorButton_Click"/>

            <!-- Row 3: numbers + multiply -->
            <Button Content="7" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="8" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="9" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="*" Background="#FF9500" Click="OperatorButton_Click"/>

            <!-- Row 4 -->
            <Button Content="4" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="5" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="6" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="-" Background="#FF9500" Click="OperatorButton_Click"/>

            <!-- Row 5 -->
            <Button Content="1" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="2" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="3" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="+" Background="#FF9500" Click="OperatorButton_Click"/>

            <!-- Row 6 -->
            <Button Content="0" Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="." Background="#3A3A3A" Click="NumberButton_Click"/>
            <Button Content="=" Background="#4CAF50" Click="ButtonEquals_Click"/>
            <Button Content="C" Background="#E53935" Click="ButtonClear_Click"/>

            <!-- Row 7 -->
            <Button Content="⌫" Background="#616161" Click="ButtonBackspace_Click"/>
            <Button Content="(" Background="#616161" Click="OperatorButton_Click"/>
            <Button Content=")" Background="#616161" Click="OperatorButton_Click"/>
            <Button Content=" " Background="Black" IsEnabled="False"/>
        </UniformGrid>
    </Grid>
</Window>
