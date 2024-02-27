#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpilib.drive
import rev
import navx

class CanMotor:
	def __init__(self,motorID):
		self.motorID=motorID
		try:
			self.motorController=rev.CANSparkMax(motorID,1)
		except:
			self.fail()
	def fail(self):
		if self.motorID != 0:
			print("ERROR IN MOTOR "+self.motorID)
	def invert(self):
		try:
			self.motorController.setInverted(True)
		except:
			self.fail()
	def set(self, speed):
		try:
			self.motorController.set(speed)
		except:
			self.fail()
	def encoder(self):
		try:
			return self.motorController.getEncoder()
		except:
			self.fail()

def control(motor,controller,input,invert=False):
	scaledInput=eval(controller+".get"+input+"()")
	scaledInput=scaledInput*abs(scaledInput)
	if invert:
		scaledInput=scaledInput*1
	motor.set(scaledInput)

def control2(motor1,motor2,controller,input,invert=False):
	control(motor1,controller,input,invert)
	control(motor2,controller,input,invert)

def controlDrive(drive,controller):
	scaledInput=controller.getX()
	scaledInput=scaledInput*abs(scaledInput)
	x=scaledInput
	scaledInput=controller.getY()
	scaledInput=scaledInput*abs(scaledInput)
	y=scaledInput
	scaledInput=controller.getZ()
	scaledInput=scaledInput*abs(scaledInput)
	z=scaledInput
	drive.driveCartesian(x,y,z)

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		"""
        This function is called upon program startup and
        should be used for any initialization code.
        """
		# init controllers
		self.joystick=wpilib.Joystick(0)
		self.ps4=wpilib.PS4Controller(1)

		# init drive motors
		self.frontLeftMotor=rev.CANSparkMax(1,1)
		self.backRightMotor=rev.CANSparkMax(2,1)
		self.frontRightMotor=rev.CANSparkMax(3,1)
		self.backLeftMotor=rev.CANSparkMax(4,1)
		self.drivetrain=wpilib.drive.MecanumDrive(self.frontLeftMotor, self.backLeftMotor, self.frontRightMotor, self.backRightMotor)
		self.frontRightMotor.setInverted(True)
		self.backRightMotor.setInverted(True)
		self.frontLeftMotor.getEncoder().setPosition(0.0)
		self.backLeftMotor.getEncoder().setPosition(0.0)
		self.frontRightMotor.getEncoder().setPosition(0.0)
		self.backRightMotor.getEncoder().setPosition(0.0)

		#init other motors
		#replace 0 with the ID for each motor used
		#for unused motors, leave ID as 0
		self.armMotor1=CanMotor(0)
		self.armMotor2=CanMotor(0)
		self.intakeMotor1=CanMotor(0)
		self.intakeMotor2=CanMotor(0)
		self.feederMotor1=CanMotor(0)
		self.feederMotor2=CanMotor(0)
		self.shooterMotor1=CanMotor(0)
		self.shooterMotor2=CanMotor(0)

	def autonomousInit(self):
		"""This function is run once each time the robot enters autonomous mode."""
		self.timer.restart()

	def autonomousPeriodic(self):
		"""This function is called periodically during autonomous."""

	def teleopInit(self):
		"""This function is called once each time the robot enters teleoperated mode."""

	def teleopPeriodic(self):
		"""This function is called periodically during teleoperated mode."""
		controlDrive(self.drivetrain,self.joystick)


	def testInit(self):
		"""This function is called once each time the robot enters test mode."""

	def testPeriodic(self):
		"""This function is called periodically during test mode."""
		


if __name__ == "__main__":
	wpilib.run(MyRobot)