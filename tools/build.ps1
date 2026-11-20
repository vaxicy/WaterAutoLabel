$csc = 'D:\CodeBuddyData\roslyn\tasks\netcore\bincore\csc.dll'
$game = 'D:\Probably Stolen\Probably Stolen_Data\Managed'
$root = Split-Path -Parent $PSScriptRoot
$out = Join-Path $root 'build\WaterAutoLabel.dll'
$names = @('mscorlib.dll','System.dll','System.Core.dll','netstandard.dll',
    'UnityEngine.dll','UnityEngine.CoreModule.dll','UnityEngine.UI.dll','UnityEngine.UIModule.dll',
    'UnityEngine.InputLegacyModule.dll','0Harmony.dll','Assembly-CSharp.dll')
$refs = $names | ForEach-Object { "-r:$(Join-Path $game $_)" }
$sources = @('WaterAutoLabelMod.cs') | ForEach-Object { Join-Path $root "src\$_" }
& dotnet $csc -nologo -target:library "-out:$out" '-langversion:latest' $refs $sources
Write-Output ("exit=" + $LASTEXITCODE)
