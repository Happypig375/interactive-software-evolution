using System.Globalization;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Box2D.NET;

const float H = 1.0f;
const float TimeStep = 1.0f / 60.0f;
const int Substeps = 4;
const int SettleSteps = 15;
const int ObserveSteps = 120;
const float Gravity = -9.80665f;
const float Friction = 0.5f;
const float PlatformSpeed = 1.0f;
const float StationaryTolerance = 0.01f * H;
const float CarryTolerance = 0.05f * H;
const float PlatformTravelTolerance = 0.01f * H;
const int RequiredSupportedSteps = 114;

var outputDirectory = PrepareOutputDirectory(args);

var stationary = RunCondition("stationary", 0.0f, outputDirectory);
var moving = RunCondition("moving", PlatformSpeed, outputDirectory);
var assembly = typeof(B2Worlds).Assembly;
var assemblyPath = assembly.Location;
var summary = new
{
    protocol = "r01-ordinary-platform-v1",
    package = new
    {
        requestedVersion = "3.1.1.557",
        assemblyVersion = assembly.GetName().Version?.ToString(),
        informationalVersion = assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion,
        assemblyFileName = Path.GetFileName(assemblyPath),
        assemblySha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(assemblyPath)))
    },
    settings = new
    {
        H,
        gravity = Gravity,
        timeStep = TimeStep,
        substeps = Substeps,
        settleSteps = SettleSteps,
        observeSteps = ObserveSteps,
        friction = Friction,
        riderMass = 1.0f,
        riderCapsuleCenterSeparation = 0.5f * H,
        riderCapsuleRadius = 0.25f * H,
        platformWidth = 4.0f * H,
        platformHeight = 0.25f * H,
        restitutionThreshold = 1.0f / 32.0f,
        requiredSupportedSteps = RequiredSupportedSteps,
        stationaryTolerance = StationaryTolerance,
        carryTolerance = CarryTolerance,
        platformTravelTolerance = PlatformTravelTolerance
    },
    stationary,
    moving,
    stationaryControlValid = stationary.Pass,
    dependencyCarryPositive = stationary.Pass && moving.Pass
};

var jsonOptions = new JsonSerializerOptions { WriteIndented = true };
var summaryPath = Path.Combine(outputDirectory, "summary.json");
File.WriteAllText(summaryPath, JsonSerializer.Serialize(summary, jsonOptions) + Environment.NewLine);
Console.WriteLine(JsonSerializer.Serialize(summary, jsonOptions));
Console.WriteLine($"summary={summaryPath}");

static string PrepareOutputDirectory(string[] arguments)
{
    if (arguments.Length != 2 || arguments[0] != "--output-dir" || string.IsNullOrWhiteSpace(arguments[1]))
    {
        Console.Error.WriteLine("Usage: nu-r01-platform --output-dir <directory>");
        throw new ArgumentException("A single non-empty --output-dir argument is required.");
    }

    var outputDirectory = Path.GetFullPath(arguments[1]);
    if (Directory.Exists(outputDirectory))
    {
        if (Directory.EnumerateFileSystemEntries(outputDirectory).Any())
        {
            throw new IOException($"Output directory must be empty: {outputDirectory}");
        }
    }
    else
    {
        Directory.CreateDirectory(outputDirectory);
    }

    return outputDirectory;
}

static ConditionResult RunCondition(string name, float observedPlatformSpeed, string outputDirectory)
{
    var trace = new List<TraceRow>(SettleSteps + ObserveSteps + 1);
    var worldDef = B2Types.b2DefaultWorldDef();
    worldDef.gravity = new B2Vec2(0.0f, Gravity);
    var world = B2Worlds.b2CreateWorld(ref worldDef);
    try
    {
        B2Worlds.b2World_SetRestitutionThreshold(world, 1.0f / 32.0f);

        var platformDef = B2Types.b2DefaultBodyDef();
        platformDef.type = B2BodyType.b2_kinematicBody;
        platformDef.position = new B2Vec2(0.0f, 0.0f);
        platformDef.linearVelocity = new B2Vec2(0.0f, 0.0f);
        platformDef.fixedRotation = true;
        platformDef.userData = "platform";
        var platform = B2Bodies.b2CreateBody(world, ref platformDef);

        var platformShapeDef = B2Types.b2DefaultShapeDef();
        platformShapeDef.material.friction = Friction;
        platformShapeDef.material.restitution = 0.0f;
        platformShapeDef.density = 0.0f;
        platformShapeDef.enableContactEvents = true;
        platformShapeDef.userData = "platform-shape";
        var platformBox = B2Geometries.b2MakeBox(2.0f * H, 0.125f * H);
        var platformShape = B2Shapes.b2CreatePolygonShape(platform, ref platformShapeDef, ref platformBox);

        var riderDef = B2Types.b2DefaultBodyDef();
        riderDef.type = B2BodyType.b2_dynamicBody;
        riderDef.position = new B2Vec2(0.0f, 0.625f * H);
        riderDef.linearVelocity = new B2Vec2(0.0f, 0.0f);
        riderDef.gravityScale = 1.0f;
        riderDef.enableSleep = true;
        riderDef.fixedRotation = true;
        riderDef.userData = "rider";
        var rider = B2Bodies.b2CreateBody(world, ref riderDef);

        var riderShapeDef = B2Types.b2DefaultShapeDef();
        riderShapeDef.material.friction = Friction;
        riderShapeDef.material.restitution = 0.0f;
        var capsuleCenterSeparation = 0.5f * H;
        var capsuleRadius = 0.25f * H;
        var capsuleArea = 2.0f * capsuleRadius * capsuleCenterSeparation + MathF.PI * capsuleRadius * capsuleRadius;
        riderShapeDef.density = 1.0f / capsuleArea;
        riderShapeDef.enableContactEvents = true;
        riderShapeDef.userData = "rider-shape";
        var riderCapsule = new B2Capsule(
            new B2Vec2(0.0f, capsuleCenterSeparation * 0.5f),
            new B2Vec2(0.0f, -capsuleCenterSeparation * 0.5f),
            capsuleRadius);
        var riderShape = B2Shapes.b2CreateCapsuleShape(rider, ref riderShapeDef, ref riderCapsule);

        for (var step = 1; step <= SettleSteps; ++step)
        {
            B2Worlds.b2World_Step(world, TimeStep, Substeps);
            trace.Add(Observe(name, "settle", step, step * TimeStep, rider, riderShape, platform, platformShape));
        }

        var initial = trace[^1];
        B2Bodies.b2Body_SetLinearVelocity(platform, new B2Vec2(observedPlatformSpeed, 0.0f));
        var supportedSteps = 0;
        for (var step = 1; step <= ObserveSteps; ++step)
        {
            B2Worlds.b2World_Step(world, TimeStep, Substeps);
            var row = Observe(name, "observe", step, (SettleSteps + step) * TimeStep, rider, riderShape, platform, platformShape);
            trace.Add(row);
            if (row.Supported) ++supportedSteps;
        }

        var final = trace[^1];
        var relativeDrift = MathF.Abs(final.RelativeX - initial.RelativeX);
        var platformTravel = final.PlatformX - initial.PlatformX;
        var pass = name == "stationary"
            ? initial.Supported && final.Supported && relativeDrift <= StationaryTolerance
            : initial.Supported && final.Supported
              && MathF.Abs(platformTravel - PlatformSpeed * 2.0f) <= PlatformTravelTolerance
              && relativeDrift <= CarryTolerance
              && supportedSteps >= RequiredSupportedSteps;

        WriteTrace(Path.Combine(outputDirectory, $"trace-{name}.csv"), trace);
        return new ConditionResult(
            name,
            observedPlatformSpeed,
            initial.Supported,
            final.Supported,
            supportedSteps,
            initial.RiderX,
            final.RiderX,
            initial.PlatformX,
            final.PlatformX,
            platformTravel,
            initial.RelativeX,
            final.RelativeX,
            relativeDrift,
            final.RiderVx,
            final.PlatformVx,
            pass);
    }
    finally
    {
        B2Worlds.b2DestroyWorld(world);
    }
}

static TraceRow Observe(
    string condition,
    string phase,
    int step,
    float logicalTime,
    B2BodyId rider,
    B2ShapeId riderShape,
    B2BodyId platform,
    B2ShapeId platformShape)
{
    var riderPosition = B2Bodies.b2Body_GetPosition(rider);
    var platformPosition = B2Bodies.b2Body_GetPosition(platform);
    var riderVelocity = B2Bodies.b2Body_GetLinearVelocity(rider);
    var platformVelocity = B2Bodies.b2Body_GetLinearVelocity(platform);
    var supported = IsSupportedBy(rider, riderShape, platformShape);
    return new TraceRow(
        condition,
        phase,
        step,
        logicalTime,
        riderPosition.X,
        riderPosition.Y,
        riderVelocity.X,
        riderVelocity.Y,
        platformPosition.X,
        platformPosition.Y,
        platformVelocity.X,
        platformVelocity.Y,
        riderPosition.X - platformPosition.X,
        supported);
}

static bool IsSupportedBy(B2BodyId rider, B2ShapeId riderShape, B2ShapeId platformShape)
{
    var capacity = B2Bodies.b2Body_GetContactCapacity(rider);
    if (capacity == 0) return false;
    var contacts = new B2ContactData[capacity];
    var count = B2Bodies.b2Body_GetContactData(rider, contacts.AsSpan(), capacity);
    var cos45 = MathF.Sqrt(0.5f);
    for (var i = 0; i < count; ++i)
    {
        var contact = contacts[i];
        var riderIsA = B2Ids.B2_ID_EQUALS(contact.shapeIdA, riderShape);
        var riderIsB = B2Ids.B2_ID_EQUALS(contact.shapeIdB, riderShape);
        var platformIsOther =
            (riderIsA && B2Ids.B2_ID_EQUALS(contact.shapeIdB, platformShape)) ||
            (riderIsB && B2Ids.B2_ID_EQUALS(contact.shapeIdA, platformShape));
        if (!platformIsOther) continue;
        if (contact.manifold.pointCount <= 0) continue;
        var normalTowardRiderY = riderIsA ? -contact.manifold.normal.Y : contact.manifold.normal.Y;
        if (normalTowardRiderY >= cos45) return true;
    }
    return false;
}

static void WriteTrace(string path, IReadOnlyList<TraceRow> rows)
{
    var invariant = CultureInfo.InvariantCulture;
    var builder = new StringBuilder();
    builder.AppendLine("condition,phase,step,logical_time,rider_x,rider_y,rider_vx,rider_vy,platform_x,platform_y,platform_vx,platform_vy,relative_x,supported");
    foreach (var row in rows)
    {
        builder.Append(row.Condition).Append(',')
            .Append(row.Phase).Append(',')
            .Append(row.Step).Append(',')
            .Append(row.LogicalTime.ToString("R", invariant)).Append(',')
            .Append(row.RiderX.ToString("R", invariant)).Append(',')
            .Append(row.RiderY.ToString("R", invariant)).Append(',')
            .Append(row.RiderVx.ToString("R", invariant)).Append(',')
            .Append(row.RiderVy.ToString("R", invariant)).Append(',')
            .Append(row.PlatformX.ToString("R", invariant)).Append(',')
            .Append(row.PlatformY.ToString("R", invariant)).Append(',')
            .Append(row.PlatformVx.ToString("R", invariant)).Append(',')
            .Append(row.PlatformVy.ToString("R", invariant)).Append(',')
            .Append(row.RelativeX.ToString("R", invariant)).Append(',')
            .AppendLine(row.Supported ? "true" : "false");
    }
    File.WriteAllText(path, builder.ToString());
}

internal sealed record TraceRow(
    string Condition,
    string Phase,
    int Step,
    float LogicalTime,
    float RiderX,
    float RiderY,
    float RiderVx,
    float RiderVy,
    float PlatformX,
    float PlatformY,
    float PlatformVx,
    float PlatformVy,
    float RelativeX,
    bool Supported);

internal sealed record ConditionResult(
    string Name,
    float PlatformSpeed,
    bool InitialSupported,
    bool FinalSupported,
    int SupportedObservationSteps,
    float InitialRiderX,
    float FinalRiderX,
    float InitialPlatformX,
    float FinalPlatformX,
    float PlatformTravel,
    float InitialRelativeX,
    float FinalRelativeX,
    float RelativeDrift,
    float FinalRiderVx,
    float FinalPlatformVx,
    bool Pass);
