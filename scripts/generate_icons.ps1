Add-Type -AssemblyName System.Drawing

function Generate-Icon([int]$size, [string]$outPath) {
    $bmp = New-Object System.Drawing.Bitmap($size, $size)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.Clear([System.Drawing.Color]::Transparent)

    # Rounded rectangle path
    $radius = [int]($size * 0.18)
    $rect = New-Object System.Drawing.Rectangle(0, 0, $size, $size)
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $d = $radius * 2

    $path.AddArc($rect.X, $rect.Y, $d, $d, 180, 90)
    $path.AddArc($rect.Right - $d, $rect.Y, $d, $d, 270, 90)
    $path.AddArc($rect.Right - $d, $rect.Bottom - $d, $d, $d, 0, 90)
    $path.AddArc($rect.X, $rect.Bottom - $d, $d, $d, 90, 90)
    $path.CloseFigure()

    $brushBg = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 90, 31))
    $g.FillPath($brushBg, $path)

    # Draw letter 'm'
    $fontSize = [float]($size * 0.58)
    $fontFamily = New-Object System.Drawing.FontFamily('Arial')
    $font = New-Object System.Drawing.Font($fontFamily, $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $brushText = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)

    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center

    # Slight vertical offset so letter 'm' is visually centered
    $textRect = New-Object System.Drawing.RectangleF(0, -($size * 0.04), $size, $size)
    $g.DrawString('m', $font, $brushText, $textRect, $sf)

    $bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Generated: $outPath"
}

Generate-Icon 192 'microtools365\icon-192.png'
Generate-Icon 512 'microtools365\icon-512.png'
