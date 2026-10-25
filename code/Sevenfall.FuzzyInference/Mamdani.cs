// Original Sevenfall max-min Mamdani inference for the OpenRA squad rule API.
// Copyright (c) 2026 Sevenfall contributors. GPL-3.0-or-later.
// No source from the unavailable OpenRA-FuzzyLogicLibrary fork is incorporated.
using System.Text.RegularExpressions;

namespace AI.Fuzzy.Library;

public sealed class TrapezoidMembershipFunction
{
    readonly double a, b, c, d;
    public TrapezoidMembershipFunction(double a, double b, double c, double d)
    {
        if (a > b || b > c || c > d) throw new ArgumentException("Unordered trapezoid points");
        (this.a, this.b, this.c, this.d) = (a, b, c, d);
    }
    public double Evaluate(double x)
    {
        if (double.IsNaN(x) || x < a || x > d) return 0;
        if (x >= b && x <= c) return 1;
        return x < b ? (x - a) / (b - a) : (d - x) / (d - c);
    }
}

public sealed class FuzzyTerm
{
    public string Name { get; }
    public TrapezoidMembershipFunction Function { get; }
    public FuzzyTerm(string name, TrapezoidMembershipFunction function) => (Name, Function) = (name, function);
}

public sealed class FuzzyVariable
{
    public string Name { get; }
    public double Minimum { get; }
    public double Maximum { get; }
    public List<FuzzyTerm> Terms { get; } = new();
    public FuzzyVariable(string name, double minimum, double maximum)
    {
        if (!(minimum < maximum)) throw new ArgumentException("Empty variable domain");
        (Name, Minimum, Maximum) = (name, minimum, maximum);
    }
}

public sealed class MamdaniFuzzyRule
{
    internal Func<Dictionary<FuzzyVariable, double>, double> Antecedent;
    internal FuzzyVariable Output;
    internal FuzzyTerm Term;
}

public sealed class MamdaniFuzzySystem
{
    public List<FuzzyVariable> Input { get; } = new();
    public List<FuzzyVariable> Output { get; } = new();
    public List<MamdaniFuzzyRule> Rules { get; } = new();
    public FuzzyVariable InputByName(string name) => Input.Single(v => v.Name == name);
    public FuzzyVariable OutputByName(string name) => Output.Single(v => v.Name == name);

    public MamdaniFuzzyRule ParseRule(string text) => new RuleParser(this, text).Parse();

    public Dictionary<FuzzyVariable, double> Calculate(Dictionary<FuzzyVariable, double> values)
    {
        foreach (var variable in Input)
            if (!values.ContainsKey(variable)) throw new ArgumentException("Missing input: " + variable.Name);
        var strengths = Rules.Select(r => (Rule: r, Strength: r.Antecedent(values))).ToArray();
        var result = new Dictionary<FuzzyVariable, double>();
        foreach (var output in Output)
        {
            var active = strengths.Where(r => r.Rule.Output == output && r.Strength > 0).ToArray();
            double mass = 0, moment = 0;
            // Trapezoidal numerical integration of the clipped output membership.
            const int intervals = 256;
            for (var i = 0; i <= intervals; i++)
            {
                var x = output.Minimum + (output.Maximum - output.Minimum) * i / intervals;
                double membership = 0;
                foreach (var rule in active)
                    membership = Math.Max(membership, Math.Min(rule.Strength, rule.Rule.Term.Function.Evaluate(x)));
                var weight = i == 0 || i == intervals ? 0.5 : 1;
                mass += membership * weight;
                moment += x * membership * weight;
            }
            result.Add(output, mass > 0 ? moment / mass : double.NaN);
        }
        return result;
    }

    sealed class RuleParser
    {
        readonly MamdaniFuzzySystem system;
        readonly string[] tokens;
        int at;
        public RuleParser(MamdaniFuzzySystem system, string text)
        {
            this.system = system;
            var matches = Regex.Matches(text, @"\(|\)|[A-Za-z][A-Za-z0-9_]*");
            tokens = matches.Select(m => m.Value).ToArray();
            if (string.Concat(tokens) != Regex.Replace(text, @"\s", ""))
                throw new ArgumentException("Unsupported fuzzy rule syntax");
        }
        string Next() => at < tokens.Length ? tokens[at++] : throw new ArgumentException("Truncated fuzzy rule");
        void Expect(string token)
        {
            if (Next() != token) throw new ArgumentException("Expected " + token);
        }
        bool Take(string token)
        {
            if (at >= tokens.Length || tokens[at] != token) return false;
            at++; return true;
        }
        internal MamdaniFuzzyRule Parse()
        {
            Expect("if"); var antecedent = Or(); Expect("then");
            var output = system.OutputByName(Next()); Expect("is");
            var name = Next(); var term = output.Terms.Single(t => t.Name == name);
            if (at != tokens.Length) throw new ArgumentException("Trailing fuzzy rule tokens");
            return new MamdaniFuzzyRule { Antecedent = antecedent, Output = output, Term = term };
        }
        Func<Dictionary<FuzzyVariable, double>, double> Or()
        {
            var left = And();
            while (Take("or"))
            {
                var previous = left; var right = And();
                left = v => Math.Max(previous(v), right(v));
            }
            return left;
        }
        Func<Dictionary<FuzzyVariable, double>, double> And()
        {
            var left = Atom();
            while (Take("and"))
            {
                var previous = left; var right = Atom();
                left = v => Math.Min(previous(v), right(v));
            }
            return left;
        }
        Func<Dictionary<FuzzyVariable, double>, double> Atom()
        {
            if (Take("(")) { var nested = Or(); Expect(")"); return nested; }
            var variable = system.InputByName(Next()); Expect("is");
            var name = Next(); var term = variable.Terms.Single(t => t.Name == name);
            return values => term.Function.Evaluate(values[variable]);
        }
    }
}
