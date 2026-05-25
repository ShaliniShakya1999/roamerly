# replace_logo.ps1
$root = "d:\project\peyug_project\roamerly"
Get-ChildItem -Path $root -Recurse -Include *.html -File | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $newContent = $content -replace '(?s)<a class="navbar-brand".*?</a>', '<a class="navbar-brand" href="index.html"><img src="assets/images/logo.png" alt="Roamerly Logo" class="navbar-logo"></a>'
    if ($newContent -ne $content) {
        Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8
        Write-Host "Updated $($_.FullName)"
    }
}
