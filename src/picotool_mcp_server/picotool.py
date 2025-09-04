"""Picotool command wrapper."""

import asyncio
import shutil
from typing import List, Optional


class PicotoolError(Exception):
    """Exception raised when picotool command fails."""
    pass


class PicotoolWrapper:
    """Wrapper for picotool command-line interface."""
    
    def __init__(self, picotool_path: Optional[str] = None) -> None:
        """Initialize picotool wrapper.
        
        Args:
            picotool_path: Path to picotool binary. If None, will search PATH.
        """
        if picotool_path is None:
            picotool_path = shutil.which("picotool")
            if picotool_path is None:
                raise PicotoolError("picotool not found in PATH. Please install picotool.")
        
        self.picotool_path = picotool_path
    
    async def _run_command(self, args: List[str]) -> str:
        """Run a picotool command and return stdout.
        
        Args:
            args: Command arguments (excluding 'picotool')
            
        Returns:
            Command stdout as string
            
        Raises:
            PicotoolError: If command fails
        """
        cmd = [self.picotool_path] + args
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode("utf-8").strip()
                raise PicotoolError(f"picotool command failed: {error_msg}")
            
            return stdout.decode("utf-8").strip()
        
        except FileNotFoundError:
            raise PicotoolError(f"picotool binary not found at: {self.picotool_path}")
        except Exception as e:
            raise PicotoolError(f"Error running picotool: {str(e)}")
    
    async def info(
        self,
        target: str = "",
        basic: bool = True,
        metadata: bool = False,
        pins: bool = False,
        device: bool = False,
        debug: bool = False,
        build: bool = False,
        all: bool = False,
        force: bool = False,
        force_no_reboot: bool = False,
        bus: Optional[str] = None,
        address: Optional[str] = None,
        vid: Optional[str] = None,
        pid: Optional[str] = None,
        serial: Optional[str] = None
    ) -> str:
        """Get device or binary information.
        
        Args:
            target: File path to analyze, or empty string for connected devices
            basic: Include basic information (default)
            metadata: Include all metadata blocks
            pins: Include pin information
            device: Include device information
            debug: Include device debug information
            build: Include build attributes
            all: Include all information
            force: Force device not in BOOTSEL mode to reset and execute command
            force_no_reboot: Force device reset but don't reboot back to application mode
            bus: Filter devices by USB bus number
            address: Filter devices by USB device address
            vid: Filter by vendor ID
            pid: Filter by product ID
            serial: Filter by serial number
            
        Returns:
            Information output from picotool
        """
        args = ["info"]
        
        # Add information option flags
        if all:
            args.append("-a")
        else:
            if basic:
                args.append("-b")
            if metadata:
                args.append("-m")
            if pins:
                args.append("-p")
            if device:
                args.append("-d")
            if debug:
                args.append("--debug")
            if build:
                args.append("-l")
        
        # Add target if specified (must come before device selection options)
        if target:
            args.append(target)
        
        # Add device selection options
        if bus:
            args.extend(["--bus", bus])
        if address:
            args.extend(["--address", address])
        if vid:
            args.extend(["--vid", vid])
        if pid:
            args.extend(["--pid", pid])
        if serial:
            args.extend(["--ser", serial])
        
        # Add force options (must be last)
        if force:
            args.append("-f")
        elif force_no_reboot:
            args.append("-F")
        
        return await self._run_command(args)
    
    async def reboot(
        self,
        all_devices: bool = False,
        usb_mass_storage: bool = False,
        partition: Optional[str] = None,
        cpu: Optional[str] = None,
        force: bool = False,
        force_no_reboot: bool = False,
        bus: Optional[str] = None,
        address: Optional[str] = None,
        vid: Optional[str] = None,
        pid: Optional[str] = None,
        serial: Optional[str] = None
    ) -> str:
        """Reboot connected Pico device(s).
        
        Args:
            all_devices: Reboot all connected devices
            usb_mass_storage: Reboot to USB mass storage mode (BOOTSEL)
            partition: Reboot to a specific partition
            cpu: Specify which CPU to boot (ARM/RISC-V for RP2350)
            force: Force device not in BOOTSEL mode to reset
            force_no_reboot: Force device reset but don't reboot back
            bus: Filter devices by USB bus number
            address: Filter devices by USB device address
            vid: Filter by vendor ID
            pid: Filter by product ID
            serial: Filter by serial number
            
        Returns:
            Reboot command output from picotool
        """
        args = ["reboot"]
        
        # Add reboot options
        if all_devices:
            args.append("-a")
        if usb_mass_storage:
            args.append("-u")
        if partition:
            args.extend(["-g", partition])
        if cpu:
            args.extend(["-c", cpu])
        
        # Add device selection options
        if bus:
            args.extend(["--bus", bus])
        if address:
            args.extend(["--address", address])
        if vid:
            args.extend(["--vid", vid])
        if pid:
            args.extend(["--pid", pid])
        if serial:
            args.extend(["--ser", serial])
        
        # Add force options (must be last)
        if force:
            args.append("-f")
        elif force_no_reboot:
            args.append("-F")
        
        return await self._run_command(args)
    
    async def version(self) -> str:
        """Get picotool version.
        
        Returns:
            Version string from picotool
        """
        return await self._run_command(["version"])