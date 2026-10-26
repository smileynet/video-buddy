# THROWAWAY: native file-preparation adaptation, fixed ordinary filenames only.
foreach ($name in @('index.html', 'app.js')) {
    if (Test-Path -LiteralPath $name) {
        if (-not (Test-Path -LiteralPath $name -PathType Leaf)) {
            throw "$name exists but is not a file. Stop and resolve the conflict."
        }
        continue
    }
    New-Item -ItemType File -Path . -Name $name -ErrorAction Stop | Out-Null
}
