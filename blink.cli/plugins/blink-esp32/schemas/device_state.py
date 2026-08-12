"""Pydantic models for tinkr-esp32-specific data shapes.

Used by the HAL adapter to validate typed data flowing between the CLI tools
and the rest of Tinkr.
"""
from typing import Literal
from pydantic import BaseModel, Field


# The 6 ESP32 family identifiers.
ESP32Family = Literal["esp32", "esp32s2", "esp32s3", "esp32c3", "esp32c6", "esp32c2"]

# The firmware types this plugin supports.
ESP32FirmwareType = Literal["micropython", "circuitpython", "esp-idf", "arduino"]


class ESP32ChipInfo(BaseModel):
    """The result of `tinkr-esp32-identify`."""
    chip: str = Field(..., description="Chip name, e.g., 'ESP32-S3'")
    family: ESP32Family = Field(..., description="Chip family, e.g., 'esp32s3'")
    chip_id: str | None = Field(None, description="Chip ID from esptool, e.g., '0x12345678'")
    mac: str | None = Field(None, description="MAC address, e.g., 'aa:bb:cc:dd:ee:ff'")
    flash_size: str | None = Field(None, description="Detected flash size, e.g., '8MB'")
    flash_address: str = Field(..., description="Default flash start address, e.g., '0x0'")
    port: str = Field(..., description="Serial port the device is on")


class ESP32PortInfo(BaseModel):
    """A detected ESP32 port from `tinkr-esp32-port-scan`."""
    port: str = Field(..., description="Serial port device path")
    vid: str | None = Field(None, description="Vendor ID, e.g., '0x303A'")
    pid: str | None = Field(None, description="Product ID, e.g., '0x0002'")
    description: str | None = None
    manufacturer: str | None = None
    interface: str | None = None


class ESP32PortScanResult(BaseModel):
    """The full result of `tinkr-esp32-port-scan`."""
    count: int = Field(..., ge=0)
    devices: list[ESP32PortInfo] = Field(default_factory=list)


class ESP32FlashRequest(BaseModel):
    """A flash request, as the HAL adapter builds it from MCP tool calls."""
    firmware_path: str = Field(..., description="Absolute path to the firmware .bin file")
    address: str | None = Field(None, description="Flash start address; auto-detect if absent")
    erase: bool = Field(False, description="Erase flash before writing")
    baud: int = Field(460800, ge=9600, le=921600, description="esptool baud rate")


class ESP32ReplResult(BaseModel):
    """The result of a single `tinkr-esp32-repl-execute` invocation."""
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0
    port: str


class ESP32FileEntry(BaseModel):
    """A single file/dir entry from `tinkr-esp32-fs-list`."""
    name: str
    type: Literal["file", "dir", "unknown"] = "unknown"
    size: int | None = None
    error: str | None = None


class ESP32FsListResult(BaseModel):
    """The full result of `tinkr-esp32-fs-list`."""
    path: str
    port: str
    entries: list[ESP32FileEntry] = Field(default_factory=list)
